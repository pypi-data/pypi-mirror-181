# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import gettext
import logging as log
import os
import socket
import subprocess
import time
from enum import Enum
from pathlib import Path

from bc_devtool import arg_actions
from bc_devtool import utils
from bc_devtool.configurator import Configurator

logging = log.getLogger(__name__)
SECURITY_GROUP_SECTION_NAME = 'security_group'
_ = gettext.translation('arg_actions', Path.joinpath(Path(__file__).parent, 'locale'), fallback=True).gettext


class AliConst:
  RegionId = 'RegionId'
  SecurityGroupId = 'SecurityGroupId'
  IpProtocol = 'IpProtocol'
  PortRange = 'PortRange'
  NicType = 'NicType'
  region = 'region'
  SourceCidrIp = 'SourceCidrIp'
  Description = 'Description'
  Priority = 'Priority'
  Policy = 'Policy'
  # 删除安全组中的一条入规则 api
  RevokeSecurityGroup = 'RevokeSecurityGroup'
  # 新增安全组入规则 api
  AuthorizeSecurityGroup = 'AuthorizeSecurityGroup'
  Domains = 'domains'
  IpList = 'ipList'


class AliRequest:
  __param = {}
  __api = ''
  command = 'ecs'

  def addParameter(self, key, value):
    self.__param['--' + key] = str(value)
    return self

  def addStringParameter(self, key, value):
    self.__param['--' + key] = "'%s'" % str(value)
    return self

  def api(self, value):
    self.__api = value
    return self

  def request(self):
    url = 'aliyun %s %s' % (self.command, self.__api)
    for k, v in self.__param.items():
      url = '%s %s %s' % (url, k, v)

    print('execute ali cli: ', url)

    success = False
    res = subprocess.Popen(url, shell=True, stdout=subprocess.PIPE)
    if res.returncode == 0:
      # 执行成功
      print('run successful')
      success = True
    else:
      lines = res.stdout.readlines()
      print(lines)
    return success


def query_domin_ip(domain):
  try:
    address = socket.getaddrinfo(domain, 'http')
    return address[0][4][0]
  except Exception as e:
    logging.error('query domin ip address failed, domain: %s, error: %s', domain, e)
  return None


def query_domain_ips(domains: list[str]) -> set[str]:
  ips = set()
  for domain in domains:
    ip = query_domin_ip(domain)
    if ip:
      ips.add(ip)
  return ips

# 读取旧的ip地址


def read_ip_list_from_file(path: Path) -> set[str]:
  """读取写入ip地址的文件,每一行一个ip地址

  Args:
      path (str): 文件路径

  Returns:
      list[str]: 读取到的 ip 集合
  """
  ips = set()
  if not path.is_file():
    return ips

  with path.open('r', encoding='utf-8') as f:
    ips.add(f.readline().strip())
  return ips


def write_ip_list(path: Path, ips: set[str]) -> None:
  with path.open('w', encoding='utf-8') as f:
    f.writelines(ips)


def change_security_rule(config: Configurator, new_ip: str, old_ip: str, add: bool) -> bool:
  # 删除旧的入口规则
  # aliyun ecs RevokeSecurityGroup --region 区域 --RegionId ID --SecurityGroupId 安全组 --IpProtocol 端口协议 --SourceCidrIp 进站ip --PortRange 端口范围
  req = AliRequest()
  req.api(AliConst.AuthorizeSecurityGroup if add else AliConst.RevokeSecurityGroup)
  req.addParameter(AliConst.region, config.get_string(AliConst.RegionId))
  req.addStringParameter(AliConst.RegionId, config.get_string(AliConst.RegionId))
  req.addStringParameter(AliConst.SecurityGroupId, config.get_string(AliConst.SecurityGroupId))
  req.addStringParameter(AliConst.PortRange, config.get_string(AliConst.PortRange))
  req.addParameter(AliConst.IpProtocol, config.get_string(AliConst.IpProtocol))
  req.addStringParameter(AliConst.SourceCidrIp, '%s/32' % (new_ip if add else old_ip))
  if add:
    req.addStringParameter(AliConst.Description, config.get_string('Description'))
  ret = req.request()

  time.sleep(1)

  # 删除拒绝规则
  # aliyun ecs RevokeSecurityGroup --region 区域 --RegionId ID --SecurityGroupId 安全组 --IpProtocol 端口协议 --SourceCidrIp 进站ip --PortRange '端口范围 --Policy drop
  # 拒绝规则不用改，每次删除指定ip规则即可
  if config.get_boolean('reject'):
    req.addStringParameter(AliConst.SourceCidrIp, '0.0.0.0/0')
    req.addParameter(AliConst.Policy, 'drop')
    req.addParameter(AliConst.Priority, '2')
    if add:
      req.addStringParameter(AliConst.Description, config.get_string('dDescription'))
    ret |= req.request()
  return ret


def remove_security_group_action(config: Configurator) -> None:
  file = config.get_object_value('file')
  old_ips = read_ip_list_from_file(file)
  new_ips = query_domain_ips(config.get_string_list(AliConst.Domains))
  new_ips += config.get_string_list(AliConst.IpList)
  for ip in old_ips + new_ips:
    if change_security_rule(config, ip, ip, False):
      logging.info('successfully removed ip rule: %s', ip)
  if os.path.isfile(file):
    os.remove(file)


def update_security_group(arg: argparse.Namespace):
  config = Configurator(Path(arg.config), section=SECURITY_GROUP_SECTION_NAME, obj=arg)
  if arg.delete:
    remove_security_group_action(arg)
    return
  old_ips = read_ip_list_from_file(arg.file)
  new_ips = query_domain_ips(config.get_string_list('domains'))
  new_ips += config.get_string_list(AliConst.IpList)
  save_ips = old_ips & new_ips
  # 添加新增的ip集合
  change_ips = new_ips - old_ips
  if len(change_ips) == 0:
    logging.info('no ip change found')
  for ip in change_ips:
    if change_security_rule(config, ip, ip, True):
      logging.info('successfully add ip rule: %s', ip)
      save_ips.add(ip)
    else:
      logging.error('Failed to add ip rule, will not save to file: %s', ip)
  # 删除旧的 ip 集合
  for ip in old_ips - new_ips:
    if change_security_rule(config, ip, ip, False):
      logging.info('Successfully delete old ip rule: %s', ip)
    else:
      # 没删除成功则继续保存到列表中
      save_ips.add(ip)
      logging.error('Failed to delete ip rule, will continue to save to file: %s', ip)
  if save_ips != old_ips:
    write_ip_list(arg.file, save_ips)


def configuration_security_group_file(arg: argparse.Namespace) -> None:
  config = Configurator(arg.out, section=SECURITY_GROUP_SECTION_NAME, obj=arg)
  if arg.config == ConfigureFeature.VIEW:
    with open(arg.out, 'r', encoding='utf-8') as f:
      logging.warning('configure content:\n %s', f.read())

  elif arg.config == ConfigureFeature.UPDATE:
    config.update_value_from_object(AliConst.RegionId)
    config.update_value_from_object(AliConst.SecurityGroupId)
    config.update_value_from_object(AliConst.IpProtocol)
    config.update_value_from_object(AliConst.PortRange)
    config.update_value_from_object(AliConst.Description)
    config.update_value_from_object('d' + AliConst.Description)
    config.update_value_from_object(AliConst.IpList)
    config.update_value_from_object(AliConst.Domains)
    config.save()
  elif arg.config == ConfigureFeature.OVERRIDE:
    config.remove_section()
    config.update_value_from_object(AliConst.RegionId)
    config.update_value_from_object(AliConst.SecurityGroupId)
    config.update_value_from_object(AliConst.IpProtocol)
    config.update_value_from_object(AliConst.PortRange)
    config.update_value_from_object(AliConst.Description)
    config.update_value_from_object('d' + AliConst.Description)
    config.update_value_from_object(AliConst.IpList)
    config.update_value_from_object(AliConst.Domains)
    config.save()
  elif arg.config == ConfigureFeature.DELETE:
    config.delete_configuration()


class ConfigureFeature(Enum):
  # 查看配置文件
  VIEW = 'view'
  # 更新配置文件
  UPDATE = 'update'
  # 强制重写配置文件
  OVERRIDE = 'override'
  # 删除配置文件
  DELETE = 'delete'


def initArgument():
  parser = argparse.ArgumentParser(formatter_class=arg_actions.DefaultsHelpFormatter,
                                   description=_('阿里云Api帮助工具,需要安装aliyun命令行工具'), conflict_handler='resolve')
  # 公共参数
  parser.add_argument('-r', '--' + AliConst.RegionId, help=_('安全组所在区域id'))
  parser.add_argument('-s', '--' + AliConst.SecurityGroupId, help=_('安全组id'))
  parser.add_argument('-i', '--' + AliConst.IpProtocol, help=_('ip协议类型'))
  parser.add_argument('-p', '--' + AliConst.PortRange, help=_('指定修改的端口'))
  parser.add_argument('-des', '--' + AliConst.Description, help=_('规则描述'))
  parser.add_argument('-ddes', '--d' + AliConst.Description, help=_('拒绝规则描述'))

  subparse = parser.add_subparsers(description=_('子命令选项'))
  # 安全组配置
  secret_group = subparse.add_parser(
      'security-group', formatter_class=arg_actions.DefaultsHelpFormatter, help=_('新增/删除安全组配置'))

  secret_group.add_argument('-c', '--config', default='security_group.config',
                            help=_('默认的安全组配置文件,默认从该文件中读取所有参数'), action=arg_actions.FileAction)
  secret_group.add_argument('-f', '--file', help=_('保存旧ip的文件路径'), default='ip.txt',
                            action=arg_actions.FileAction, must_exist=False)
  secret_group.add_argument('-d', '--delete', help=_('强制删除ip配置'), action='store_true')
  secret_group.add_argument('-j', '--reject', help=_('同时删除或添加拒绝规则'), action='store_true')
  secret_group.add_argument('--' + AliConst.IpList, nargs='*', help=_('允许的ip地址列表'))
  secret_group.add_argument(AliConst.Domains, help='允许的域名集合', nargs='*')
  secret_group.set_defaults(func=update_security_group)

  # 配置文件生成
  config_group = subparse.add_parser(
      'configure', formatter_class=argparse.ArgumentDefaultsHelpFormatter, help=_('配置安全组配置文件'))
  config_group.add_argument('-o', '--out', default='security_group.config', help=_('输出的配置文件'),
                            action=arg_actions.FileAction, must_exist=False)
  config_group.add_argument('-c', '--config', action=arg_actions.EnumAction,
                            type=ConfigureFeature, help=_('选择执行的操作'), default=ConfigureFeature.VIEW)
  config_group.add_argument('--' + AliConst.IpList, nargs='*', type=list[str], help=_('默认的固定ip集合,不再走域名查询'))
  config_group.add_argument(AliConst.Domains, nargs='*', help=_('默认配置的域名'))
  config_group.set_defaults(func=configuration_security_group_file)

  try:
    options = parser.parse_args()
    options.print_help = parser.print_help
    return options
  except (ValueError, TypeError) as e:
    logging.fatal(e.args[0])


def main():
  utils.init_color()
  args = initArgument()
  if hasattr(args, 'func'):
    args.func(args)
  else:
    args.print_help()


if __name__ == '__main__':
  try:
    main()
  except FileNotFoundError as e:
    logging.error(e)
  except KeyboardInterrupt:
    pass
