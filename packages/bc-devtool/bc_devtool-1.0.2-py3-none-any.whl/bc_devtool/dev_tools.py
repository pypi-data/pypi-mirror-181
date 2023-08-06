# -*- coding: utf-8 -*-
# /usr/bin/python3
from __future__ import annotations

import argparse
import enum
import gettext
import logging
import os
import re
from enum import auto
from enum import Enum
from enum import unique
from pathlib import Path
from typing import List

import bc_devtool
from bc_devtool import arg_actions as aa
from bc_devtool import file_util
from bc_devtool import utils
from bc_devtool.utils import simple_log
from git import Repo


VERSION = bc_devtool.__version__
_ = gettext.translation('dev_tools', Path.joinpath(Path(__file__).parent, 'locale'), fallback=True).gettext
REPO_PATH = '.repo/manifests/default.xml'
recore_error = None

SOURCE_SUFFIXS = ['cpp', 'cc', 'c', 'h', 'hpp', 'txt', 'py', 'cmake', 'java']


def filter_non_project_file(path: str):
  """过滤常见非项目的文件

  Args:
      path (str): 文件路径名

  Returns:
      bool: 是项目文件返回True,否则返回False
  """
  filter_suffix = ['.class', '.project', '.mp4', '.rawproto', '.html', '.bin']
  filter_path = ['.vscode', '.gradle']
  for name in filter_path:
    if path.find(name) != -1:
      return False
  for suffix in filter_suffix:
    if path.endswith(suffix):
      return False
  return True


def read_android_repo_all_git_project(base: Path) -> List[str]:
  """读取android源码的 manifest 文件获取所有git项目

  Args:
      base (Path): android源码根路径

  Returns:
      List[str]: 所有 git 项目路径
  """

  path = base.joinpath(REPO_PATH)
  projects = []
  if not path.is_file():
    simple_log.error('android manifest file not exist: %s', path)
    return projects

  def handle_line(line):
    res = re.search('path=\\"(.*?)\\"', line, 0)
    if res:
      projects.append(res.group(1))

  file_util.visit_file_line(path, handle_line)
  return projects


def init_error_file(path: str):
  global recore_error
  if path:
    p = Path(path).resolve()
    file_util.make_sure_file_path(str(p))
    recore_error = utils.get_logger_file(str(p))
  else:
    recore_error = logging.getLogger('Error')
  recore_error.setLevel(logging.DEBUG)


def read_all_child_directories(arg):
  ms = []
  if arg.childs != None:
    ms.extend(arg.childs)
  if arg.file != None:
    ms.extend(file_util.read_file_to_lines(arg.file))
  if arg.android != None:
    ms.extend(read_android_repo_all_git_project(arg.root))
  return list(set(ms))


def git_checkout_file_permission(base_dir: Path, dirs: list[str]):
  for dir in dirs:
    path = base_dir.joinpath(dir.strip()).resolve()
    if not path.is_dir():
      simple_log.warning('is not a valid directory: ', path)
      continue
    try:
      for item in Repo(str(path)).index.diff(None).iter_change_type('M'):
        if item.b_mode != item.a_mode:
          path = path.joinpath(item.a_path)
          path.chmod(item.a_mode)
          simple_log.warning('restore file mode: %s, new mode: %o, old mode: %o', path, item.b_mode, item.a_mode)
    except Exception as e:
      simple_log.exception('fix file mode error: %s', e)
      recore_error.exception('%s', e)


def restore_git_directories_permission(arg):
  """恢复git仓库文件权限的改变,这在跨操作系统时常用

  Args:
      arg (object): 参数对象
  """
  dirs = read_all_child_directories(arg)
  git_checkout_file_permission(arg.root, dirs)


def git_diff_file_of_project(base_dir: Path, dir: str, out, restore=False):
  # 获取所有git仓库修改的文件和新增的文件
  path = base_dir.joinpath(dir.strip()).resolve()
  logging.debug('git diff path: %s, exist: %s', path, path.is_dir())
  if not path.is_dir():
    simple_log.error('path is not a directory: %s', path)
    return

  try:
    repo = Repo(str(path))
    has_write_head = False
    for item in repo.index.diff(None):
      p = path.joinpath(item.a_path)
      if filter_non_project_file(item.a_path):
        if not has_write_head:
          out.debug('===> project diff: %s\n', path)
          has_write_head = True
        out.debug('type: %s, path: %s', (item.change_type, p))

      if item.change_type == 'D':
        # 删除文件
        if restore:
          repo.index.checkout(item.a_path)
          logging.debug('restore deleted files: %s', item.a_path)
        continue
      elif item.change_type == 'A':
        logging.debug('found new file: %s', p)

    # 处理未跟踪文件
    for item in repo.untracked_files:
      if filter_non_project_file(item):
        p = path.joinpath(item)
        logging.debug('found untracked file: %s', p)
        if not has_write_head:
          out.debug('===> project untracked file: %s\n', p)
          has_write_head = True
        out.debug('untracked file: %s', p)
  except Exception as e:
    simple_log.exception('git diff repo error: %s', e)
    recore_error.debug(str(e))


def git_diff_all_project(arg):
  """获取git仓库的修改文件和新增文件

  Args:
      base_dir (str): 仓库根目录
      dir (str): 相对于根目录的子目录路径
      out (str): 保存 diff 到文件
      restore (bool, optional): 是否要恢复该文件. 默认为: False.
  """
  dirs = read_all_child_directories(arg)
  if len(dirs) == 0:
    dirs = ['']
  out = utils.get_logger_file(arg.out)
  for dir in dirs:
    git_diff_file_of_project(arg.root, dir, out, arg.restore)


def open_windows_case_sensitive(arg):
  """递归开启 windows 目录的大小写敏感,目录已经存在时设置不会影响子目录,因此需要递归设置
  需要 管理员权限 运行

  Args:
      arg (object): 传入参数
  """
  cmd = 'fsutil.exe file SetCaseSensitiveInfo %s ' + ('enable' if arg.disable else 'disable')
  logging.error(cmd)
  for dir in arg.dirs:
    for sub_dir in dir.rglob('**/'):
      os.system(cmd % str(sub_dir))

# 合并多个文件为一个


def merge_files_to_file(arg):
  """多个文件合并为一个

  Args:
      arg (object): 合并参数
  """
  file_util.merge_multiple_files(
      arg.files, arg.out, not arg.binary, arg.append)


@unique
class FileEncoding(Enum):
  UTF8 = 'utf-8'
  UTF8_DOM = 'utf-8-sig'


@unique
class EncodingTransform(enum.Flag):
  # 查看文件编码
  VIEW = auto()
  # 已知编码的转换
  TRANSFORM_KNOWN = auto()
  # 自动检测的编码转换
  TRANSFORM_AUTO = auto()
  CRLF_TO_LF = auto()
  LF_TO_CRLF = auto()
  CN_TRANSFORM = auto()


def handle_file_encoding(arg):
  # 输出路径与输入路径对应,如果输入是目录则输出也是目录
  out_path = Path(arg.out).resolve() if arg.out else None
  out_base = None

  def walk_file(root: Path, file: Path):
    suffix = file.suffix
    if len(suffix) == 0 or suffix[0] != '.':
      return
    # 过滤文件类型
    if suffix[1:] not in arg.suffixs:
      return

    output = Path.joinpath(out_path, file.relative_to(out_base)) if root and out_path else out_path
    converter = None
    for cmd in arg.cmd:
      if cmd == EncodingTransform.VIEW:
        best = file_util.get_file_encoding(file)
        simple_log.info('file: %s, encoding: %s', file, best)
      else:
        if converter is None:
          converter = file_util.FileConverter(input=file, out=output, no_change_copy_file=arg.copy)
        # 先转换编码,再替换字节
        if cmd == EncodingTransform.TRANSFORM_KNOWN:
          converter.from_encoding = getattr(arg, 'from').value
          converter.to_encoding = getattr(arg, 'to').value
          converter.add_action(file_util.FileConvertAction.transform_encoding)
        elif cmd == EncodingTransform.TRANSFORM_AUTO:
          converter.to_encoding = getattr(arg, 'to').value
          converter.add_action(file_util.FileConvertAction.transform_encoding)
        elif cmd == EncodingTransform.CN_TRANSFORM:
          converter.to_encoding = getattr(arg, 'to').value
          converter.add_action(file_util.FileConvertAction.chinese_transform_encoding)
        elif cmd == EncodingTransform.CRLF_TO_LF:
          converter.add_action(file_util.FileConvertAction.crlf_to_lf)
        if cmd == EncodingTransform.LF_TO_CRLF:
          converter.add_action(file_util.FileConvertAction.lf_to_crlf)

    if converter:
      res = converter.execute()
      if res.is_failed():
        simple_log.error(res.failed_reson)
      else:
        logging.info('handler file success: %s', file)

  def handle_dir(file: Path):
    nonlocal out_base
    out_base = file.resolve()
    for sub_file in (file.rglob('*') if arg.recursive else file.glob('*')):
      if sub_file.is_file():
        walk_file(file, sub_file)

  for file in arg.files:
    if file.is_dir():
      handle_dir(file)
    elif file.is_file():
      walk_file(None, file)
    elif file.is_symlink():
      file = file.readlink()
      if file.is_dir():
        handle_dir(file)
      elif file.is_file():
        walk_file(None, file)


def init_arguments():
  parser = argparse.ArgumentParser(formatter_class=aa.DefaultsHelpFormatter,
                                   description=_('日常开发小工具'), conflict_handler='resolve')
  parser.add_argument('-o', '--out', help=_('设置输出文件或目录,不同子命令输出格式不同'))

  subparsers = parser.add_subparsers(description=_('可选的子命令'))

  cmd_c = subparsers.add_parser('case-sensitive', help=_('递归开启或关闭windows目录大小写敏感, 需要管理员权限'),
                                formatter_class=aa.DefaultsHelpFormatter)
  cmd_c.add_argument('dirs', nargs='*', help=_('更改的目录'), default=[os.getcwd()], action=aa.PathAction)
  cmd_c.add_argument('-d', '--disable', action='store_true', help=_('关闭大小写敏感'))
  cmd_c.set_defaults(func=open_windows_case_sensitive)

  cmd_x = subparsers.add_parser('restore-per', help=_('恢复git仓库下所有文件权限的变化,通常用于文件跨操作系统时丢失权限'),
                                formatter_class=aa.DefaultsHelpFormatter)

  cmd_x.add_argument('root', help=_('恢复git仓库的根目录,没有子目录则只处理当前git仓库'), default=os.getcwd(), action=aa.DirectoryAction)
  cmd_x.add_argument('-c', '--childs', action='extend', nargs='+', type=str, help=_('多个git子模块目录,相对于根目录的位置'))
  cmd_x.add_argument(
      '-f', '--file', help=_('包含多个子模块的文件,每一行是一个相对与根目录的子路径'), action=aa.FileAction)
  cmd_x.add_argument('-a', '--android', action='store_true', help=_('根目录是Android源码目录,通过读取repo/manifest文件中解析出所有子目录'))
  cmd_x.set_defaults(func=restore_git_directories_permission)

  cmd_d = subparsers.add_parser('diff', help=_('读取git模块的更改,保存改变或恢复文件等等'), formatter_class=aa.DefaultsHelpFormatter)
  cmd_d.add_argument('root', help=_('git仓库根目录,没有子目录则只处理当前git仓库'), default=os.getcwd(), action=aa.PathAction)
  cmd_d.add_argument('-c', '--childs', action='extend', nargs='+', type=str, help=_('多个git子模块目录,相对于根目录的位置'))
  cmd_d.add_argument('-f', '--file', help=_('包含多个子模块的文件,每一行是一个相对与根目录的子路径'), action=aa.FileAction)
  cmd_d.add_argument('-o', '--out', help=_('将输出写入到文件'))
  cmd_d.add_argument('-r', '--restore', action='store_true', help=_('恢复已删除的文件'))
  cmd_d.add_argument('-a', '--android', action='store_true', help=_('根目录是Android源码目录,通过读取repo/manifest文件中解析出所有子目录'))
  cmd_d.set_defaults(func=git_diff_all_project)

  cmd_m = subparsers.add_parser('merge', help=_('合并多个文件为单个文件,默认为二进制模式合并'), formatter_class=aa.DefaultsHelpFormatter)
  cmd_m.add_argument('out', help=_('合并后输出的文件'))
  cmd_m.add_argument('-b', '--binary', action='store_true', help=_('以二进制模式合并,默认是文本模式'))
  cmd_m.add_argument('-f', '--files', nargs='+', help=_('指定要合并的文件集合'), action=aa.FileAction)
  cmd_m.add_argument('-a', '--append', action='store_true', help=_('增量模式,添加内容到输出文件的末尾'))
  cmd_m.set_defaults(func=merge_files_to_file)

  cmd_e = subparsers.add_parser('encoding', help=_('修改、转换文件编码'), formatter_class=aa.DefaultsHelpFormatter)

  encoding_choices_help = {
      'view': _('查看文件编码'),
      'transform_known': _('已知文件编码转换其它编码'),
      'transform_auto': _('自动检测文件编码转换'),
      'crlf_to_lf': _('CRLF 换行转 LF 换行'),
      'lf_to_crlf': _('LF 换行转 CRLF 换行'),
      'cn_transform': _('检测中文文件编码转换')
  }

  command_action: aa.TrueRequiredAction = cmd_e.add_argument('--cmd', type=EncodingTransform, action=aa.TrueRequiredAction,
                                                             action_type=aa.EnumAction,
                                                             help='\n\n'.join('{}: {}'.format(key, value)
                                                                              for key, value in encoding_choices_help.items()),
                                                             default=[EncodingTransform.VIEW], nargs='*')

  cmd_e.add_argument('files', nargs='*', default=[os.getcwd()], help=_('处理的文件集合'), action=aa.PathAction)
  cmd_e.add_argument('--recursive', action=argparse.BooleanOptionalAction, default=True, help=_('递归处理目录'))

  from_action = cmd_e.add_argument('-f', '--from', action=aa.EnumAction, type=FileEncoding, help=_('转换前的编码'))
  to_action = cmd_e.add_argument('-t', '--to', action=aa.EnumAction, type=FileEncoding, help=_('转换后的编码'))

  cmd_e.add_argument('-s', '--suffixs', nargs='*', help=_('过滤指定文件后缀名'), default=SOURCE_SUFFIXS)
  cmd_e.add_argument('--copy', action='store_true', help=_('文件未改变时复制文件,默认不复制'))

  # 因为参数是小写的,所以这里要传小写
  command_action.add_required(EncodingTransform.TRANSFORM_KNOWN.name.lower(), from_action, to_action)
  command_action.add_required(EncodingTransform.TRANSFORM_AUTO.name.lower(), to_action)
  command_action.add_required(EncodingTransform.CN_TRANSFORM.name.lower(), to_action)

  cmd_e.add_argument('-o', '--out', help=_('输出文件或目录,与输入类型对应,当传递多个文件/目录时输出可能会被覆盖'))
  cmd_e.set_defaults(func=handle_file_encoding)

  parser.add_argument('-v', '--version', action='version', version=_('实用的命令帮助 %(prog)s 版本: ') + VERSION)
  parser.add_argument('--error', help=_('错误日志输出到文件'))

  try:
    options = parser.parse_args()
    options.print_help = parser.print_help
    return options
  except (ValueError, TypeError) as e:
    logging.fatal(e.args[0])


def main():
  utils.init_color(level=logging.INFO, format='%(levelname)s: %(message)s')
  args = init_arguments()
  init_error_file(args.error)
  if hasattr(args, 'func'):
    args.func(args)
  else:
    args.print_help()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
