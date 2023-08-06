# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import gettext
import hashlib
import logging as log
import subprocess
from pathlib import Path

from bc_devtool import arg_actions as aa
from bc_devtool import configurator
from bc_devtool import utils
from bc_devtool.utils import simple_log

if utils.is_windows():
  import winreg

logging = log.getLogger(__name__)

_ = gettext.translation('arg_actions', Path.joinpath(Path(__file__).parent, 'locale'), fallback=True).gettext

DEFAULT_KEY = 'testkey.pk8'
DEFAULT_PEM = 'testkey.x509.pem'
DEFAULT_JAVA_OPT = '-Xmx1024M -Xss1m'
DEFAULT_SIGN_JAR = 'apksigner.jar'
SECTION_SIGN = 'menu_sign'
MENU_COMMAND_NAME = '*\\shell\\devtools'
DEFAULT_MENU_CMD = 'bc-devtool-menu'


class SignatureElement(aa.BaseSerialization):
  args = {
      'key': aa.ArgumentBean(ty=aa.FileAction, help=_('指定签名私钥文件,如果有密码则需要指定 key-pass,必须是 PKCS #8 DER 格式'),
                             tips=_('配置签名私钥文件,签名 APK/AAB/JAR 包使用'), must_exist=True, at_config=True),
      'key_pass': aa.ArgumentBean(ty=str, short_key=None, help=_('私钥文件需要密码时指定'), tips=_('指定签名文件所需的密码'), at_config=True),
      'cert': aa.ArgumentBean(ty=aa.FileAction, help=_('指定证书链,必须是 x509.pem或der格式'), must_exist=True, at_config=True),
      'signjar': aa.ArgumentBean(ty=aa.FileAction, help=_('指定 apksigner.jar 的路径,默认从当前执行目录查找'), must_exist=True, at_config=True),
      'zipalign': aa.ArgumentBean(ty=aa.FileAction, help=_('指定 zipalign.exe 的路径,签名时自动对齐apk'), must_exist=True, at_config=True),
      'replace': aa.ArgumentBean(help=_('输出文件替换输入文件'), at_config=True),
      'output': aa.ArgumentBean(ty=aa.FileAction, help=_('指定输出文件路径,未指定则在输入文件名后加上 .sign 后缀')),
      'print': aa.ArgumentBean(ty=bool, help=_('查看apk,jar,aab文件签名')),
      'input': aa.ArgumentBean(ty=aa.FileAction, help=_('输入的apk,jar,aab文件路径'), must_exist=True, positional=True),
  }

  def __init__(self) -> None:
    super().__init__()

  def init_default_value(self):
    config = configurator.Configurator(file_priority=True, section=SECTION_SIGN)
    parent_dir = Path(__file__).parent.resolve()
    self.key = config.get_file(key='key', fallback=parent_dir.joinpath(DEFAULT_KEY))
    self.key_pass = None
    self.cert = config.get_file(key='cert', fallback=parent_dir.joinpath(DEFAULT_PEM))
    self.signjar = config.get_file(key='signjar', fallback=parent_dir.joinpath(DEFAULT_SIGN_JAR))
    self.zipalign = config.get_file(key='zipalign', fallback=parent_dir.joinpath(
        'zipalign.exe' if utils.is_windows else 'zipalign'))
    self.replace = config.get_boolean(key='replace', fallback=False)
    self.input: Path = None
    self.output: Path = None
    self.print: bool = False


def get_options_menu(name, shell):
  key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, MENU_COMMAND_NAME)
  try:
    winreg.SetValueEx(key, 'MUIVerb', 0, winreg.REG_SZ, name + '(&T)')
    winreg.SetValueEx(key, 'SubCommands', 0, winreg.REG_SZ, '')
    winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, '%s.exe' % shell)
    logging.info(_('创建上下文菜单: %s'), name)
  except FileNotFoundError:
    pass
  return key


def set_option_subcommand(main_munu: winreg.HKEYType, index: int, name: str, cmd: str):
  menu = winreg.CreateKey(main_munu, 'shell\\{:02d}menu'.format(index))
  winreg.SetValueEx(menu, 'MUIVerb', 0, winreg.REG_SZ, name)
  key = winreg.CreateKey(menu, 'command')
  winreg.SetValueEx(key, None, 0, winreg.REG_SZ, cmd)
  logging.info('set menu command name: %s, value: %s', name, cmd)
  winreg.CloseKey(key)
  winreg.CloseKey(menu)


def run_cmd(cmd) -> bool:
  return subprocess.call(cmd, shell=True, encoding='utf-8') == 0


def run_apk_signature(options: SignatureElement):
  if not options.signjar.is_file():
    logging.fatal(_('默认签名jar文件无效: %s'), options.signjar)

  if options.print:
    simple_log.info(_('输入文件: %s'), options.input)
    cmd = f'java {DEFAULT_JAVA_OPT} -jar {options.signjar} verify --print-certs "{options.input}"'
    run_cmd(cmd)
    return

  if not options.output:
    if options.replace:
      options.output = options.input
    else:
      options.output = options.input.with_suffix('.sign' + options.input.suffix)
  # 新签名可能会产生 .idsig文件,通常不需要直接删除它
  idsig = options.output.with_suffix(options.output.suffix + '.idsig')

  if not options.key.is_file():
    logging.fatal(_('默认私钥文件无效: %s'), options.key)

  if not options.cert.is_file():
    logging.fatal(_('默认证书链文件无效: %s'), options.cert)

  password = ''
  if options.key_pass:
    password = '--key-pass ' + options.key_pass

  if options.zipalign:
    cmd = f'{options.zipalign} -f -p 4 "{options.input}" "{options.input}.align"'
    if not run_cmd(cmd):
      logging.fatal(_('对齐apk错误'))
    new_input = options.input.parent / (options.input.name + '.align')
    new_input.replace(options.input)
  cmd = f'java {DEFAULT_JAVA_OPT} -jar {options.signjar} sign --key {options.key} --cert {options.cert} {password} --in "{options.input}" --out "{options.output}"'
  if run_cmd(cmd):
    if idsig.is_file():
      idsig.unlink()


def calc_file_hash(input: Path):
  with input.open('rb') as f:
    simple_log.info(_('输入文件: %s'), input)
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha224 = hashlib.sha224()
    sha256 = hashlib.sha256()
    sha384 = hashlib.sha384()
    sha512 = hashlib.sha512()

    chunk = f.read(4096)
    while chunk:
      md5.update(chunk)
      sha1.update(chunk)
      sha224.update(chunk)
      sha256.update(chunk)
      sha384.update(chunk)
      sha512.update(chunk)
      chunk = f.read(4096)

    simple_log.info('    MD5    : %s', md5.hexdigest().upper())
    simple_log.info('    SHA1   : %s', sha1.hexdigest().upper())
    simple_log.info('    SHA224 : %s', sha224.hexdigest().upper())
    simple_log.info('    SHA256 : %s', sha256.hexdigest().upper())
    simple_log.info('    SHA384 : %s', sha384.hexdigest().upper())
    simple_log.info('    SHA512 : %s', sha512.hexdigest().upper())


def run_file_hash_cmd(options):
  for file in options.input:
    calc_file_hash(file)


def delete_menu_recursive(parent: winreg.HKEYType, sub_key: str):
  try:
    key = winreg.OpenKeyEx(parent if parent else winreg.HKEY_CLASSES_ROOT,
                           sub_key, 0, winreg.KEY_READ | winreg.KEY_WRITE)
  except OSError:
    return

  def iter_key():
    index = 0
    try:
      while True:
        yield winreg.EnumKey(key, index)
        index += 1
    except OSError:
      pass

  for item in iter_key():
    # 键可能还有子键
    delete_menu_recursive(key, item)

  winreg.DeleteKey(parent if parent else winreg.HKEY_CLASSES_ROOT, sub_key)
  logging.info(_('删除键: %s'), sub_key)


def run_menu_cmd(options):
  if options.delete:
    delete_menu_recursive(None, MENU_COMMAND_NAME)
  else:
    # 需要检测 shell 是否存在
    shell_call = {
        'cmd': 'cmd /c "{cmd} {param} "{input}""',
        'powershell': 'powershell "{cmd} {param} \'{input}\'"',
        'pwsh': 'pwsh -Command "{cmd} {param} \'{input}\'"',
        'bash': 'bash -c "{cmd} {param} {input}"',
        'sh': 'sh -c "{cmd} {param} {input}"',
    }

    shell_noexit_call = {
        'cmd': 'cmd /k "{cmd} {param} "{input}""',
        'powershell':  'powershell -NoExit "{cmd} {param} \'{input}\'"',
        'pwsh': 'pwsh -NoExit -Command "{cmd} {param} \'{input}\'"',
        'bash': shell_call.get('bash'),
        'sh': shell_call.get('sh'),
    }

    cmd = shell_call.get(options.shell, None)
    if cmd is None:
      simple_log.fatal(_('不支持的 shell,无法自动调用 shell 命令: %s'), options.shell)
    else:
      try:
        subprocess.call(cmd.format(cmd='echo', param='supported', input=''))
      except Exception as e:
        simple_log.fatal(_('不存在指定 shell (\'%s\'), 如果确定存在请将它添加到环境变量中\n错误如下:\n%s'), options.shell, e)

    main_menu = get_options_menu(options.name, options.shell)
    # 添加hash菜单
    cmd_noexit = shell_noexit_call.get(options.shell, '')
    set_option_subcommand(main_menu, 1, _('计算文件Hash(&H)'), cmd_noexit.format(
        cmd=DEFAULT_MENU_CMD, param='hash', input='%1'))
    set_option_subcommand(main_menu, 2, _('签名文件(&P)'), cmd.format(cmd=DEFAULT_MENU_CMD, param='sign', input='%1'))
    set_option_subcommand(main_menu, 3, _('查看签名(&S)'), cmd_noexit.format(
        cmd=DEFAULT_MENU_CMD, param='sign --print', input='%1'))
    if options.jadx:
      set_option_subcommand(main_menu, 4, _('打开至jadx(&J)'), cmd.format(cmd=options.jadx, param='', input='%1'))
    winreg.CloseKey(main_menu)
  pass


def check_configure_path(path: Path, is_local: bool):
  return True


def find_lastest_build_tools(sdk: Path) -> Path:
  build_tools = sdk / 'build-tools'
  max_version = 0
  tools_dir = None
  for file in build_tools.rglob('**/source.properties'):
    for line in file.read_text('utf-8').splitlines():
      if line.startswith('Pkg.Revision='):
        version_str = line.split('=')[1].split(' ')[0].split('.')
        version = int(version_str[0]) * 100 + int(version_str[1]) * 10 + int(version_str[2])
        if version > max_version:
          max_version = version
          tools_dir = file.parent
        break
  return tools_dir


def find_file_from_directory(dir: Path, pattern: str) -> Path:
  if not dir:
    return None
  for file in dir.rglob(pattern):
    return file
  return None


def set_menu_config(options: argparse.Namespace):
  if options.delete or options.unset_all or options.unset:
    configurator.change_configure(options)
    return
  if options.sdk:
    tools_dir = find_lastest_build_tools(options.sdk)
    zipalign = find_file_from_directory(tools_dir, '**/zipalign.exe' if utils.is_windows else '**/zipalign')
    if zipalign:
      options.key = 'zipalign'
      options.value = zipalign
      logging.info('found zipalign path from sdk: %s', zipalign)
      configurator.change_configure(options)
    apksigner = find_file_from_directory(tools_dir, '**/apksigner.jar')
    if apksigner:
      options.key = 'signjar'
      options.value = apksigner
      logging.info('found apksigner path from sdk: %s', apksigner)
      configurator.change_configure(options)
  else:
    configurator.change_configure(options)


def init_arguments():
  parser = argparse.ArgumentParser(description=_('windows上下文快捷菜单'),
                                   formatter_class=aa.DefaultsHelpFormatter, conflict_handler='resolve')
  parser.add_argument('-v', '--verbose', help=_('输出更详细的日志'), action='store_true')

  sub_parser: aa.SubArgumentsAction = parser.add_argument('options', action=aa.TopSubArgumentsAction, help=_('可选的子功能'))
  sub_parser.set_program_name(parser)

  cmd_sign = sub_parser.add_parser('sign', help=_('签名apk,jar,aab等文件 (默认动作)'), formatter_class=aa.DefaultsHelpFormatter)
  aa.add_object_to_argument(cmd_sign, SignatureElement)

  cmd_sign.set_defaults(func=run_apk_signature)
  config_parser = configurator.add_global_config_argument(
      parser, sub_parser, help=_('修改windows上下文菜单配置'), section=SECTION_SIGN, hide_keys=['sdk'])

  config_parser.add_argument('--sdk', help=_('设置 Android SDK 路径,自动查找所需的工具'), action=aa.DirectoryAction)
  config_parser.set_defaults(func=set_menu_config)

  dex_cmd = sub_parser.add_parser('dex', help=_('android dex/apk/aar 等文件处理'), formatter_class=aa.DefaultsHelpFormatter)

  hash_cmd = sub_parser.add_parser('hash', help=_('计算文件 hash 值'), formatter_class=aa.DefaultsHelpFormatter)
  hash_cmd.add_argument('input', nargs='+', help=_('输入文件'), action=aa.FileAction)
  hash_cmd.set_defaults(func=run_file_hash_cmd)

  menu_cmd = sub_parser.add_parser('menu', help=_('注册/删除右键菜单,需要管理员权限运行'), formatter_class=aa.DefaultsHelpFormatter)
  menu_cmd.add_argument('-n', '--name', help=_('右键菜单名称'), default=_('开发者工具'))
  menu_cmd.add_argument('-d', '--delete', action='store_true', help=_('删除注册菜单'))
  menu_cmd.add_argument('-s', '--shell', help=_('选择使用的 shell, 根据自身系统的安装情况选择'),
                        choices=['cmd', 'pwsh', 'powershell'], default='pwsh')
  menu_cmd.add_argument('--jadx', help=_('设置快速 jadx 打开 apk'), action=aa.FileAction)
  menu_cmd.set_defaults(func=run_menu_cmd)

  try:
    options = parser.parse_args()
    options.check_configure_path = check_configure_path
    options.view_config_option = SignatureElement
    return options
  except (ValueError, TypeError) as e:
    logging.fatal(e.args[0])


def main():
  try:
    utils.init_color()
    utils.simple_logging_level()
    if not utils.is_windows():
      logging.error('Only supports windows system')
      return
    options = init_arguments()
    if options.verbose:
      logging.setLevel(log.DEBUG)
    if hasattr(options, 'func'):
      options.func(options)
    else:
      options.print_help()
  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  main()
