# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import configparser
import gettext
from ctypes import ArgumentError
from pathlib import Path
from pathlib import PurePath
from typing import Any
from typing import Type
from typing import TypeVar

from bc_devtool import arg_actions as aa
from bc_devtool import utils
from bc_devtool.utils import simple_log

_ = gettext.translation('configurator', Path.joinpath(Path(__file__).parent, 'locale'), fallback=True).gettext
AT = TypeVar('AT', bound=argparse.Action)

_UNSET = object()
ST = TypeVar('ST', bound=aa.BaseSerialization)
DEFAULTSECT = configparser.DEFAULTSECT


class ConfigParserChain():
  """配置解析工具链,与 configparser 相比可以设置多个配置文件,
  依此读取配置文件中的值
  """

  @staticmethod
  def write_to_file(config: configparser.ConfigParser, path: Path, space_around_delimiters=True) -> None:
    if config is None:
      raise ArgumentError(_('写入空配置错误: {}').fromat(path))
    with path.open('w', encoding='utf-8') as f:
      config.write(f, space_around_delimiters)

  @staticmethod
  def section_set_value(config: configparser.ConfigParser, section: str, option: str, value: str = None) -> None:
    """设置节区值,如果没有该节区则创建

    Args:
        config (ConfigParser): 配置对象
        section (str): 节区名
        option (str): 选项名
        value (str, optional): 选项值. 默认是: None
    """
    if not config.has_section(section) and section != DEFAULTSECT:
      config.add_section(section)
    config.set(section, option, str(value))

  @staticmethod
  def remove_config_option(config: configparser.ConfigParser, section: str, option: str) -> bool:
    return config.remove_option(section, option)

  def remove_config_section(config: configparser.ConfigParser, section: str) -> bool:
    return config.remove_section(section)

  def overload_config(self, config: configparser.ConfigParser, overload_section=DEFAULTSECT) -> None:
    path = config.get(overload_section, 'overload_file', fallback=None)
    if not path:
      return
    self.add_config_path(Path(path), False, True, overload_section)

  def add_config_path(self, path: Path, create=False, overload=False, overload_section=DEFAULTSECT) -> None:
    if not hasattr(self, '_configs'):
      self._configs: list[configparser.ConfigParser] = []
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    files = config.read(path, encoding='utf-8')
    # 配置文件不存在则忽略它
    if len(files) == 0:
      if not create:
        return
      # 创建一个空的配置文件
      ConfigParserChain.write_to_file(config, path)
    # 添加路径属性,方便后续保存和比较路径
    config.path = path
    self._configs.insert(0, config)
    if overload:
      self.overload_config(config, overload_section)

  def get(self, section, option, raw=False, vars=None, fallback=_UNSET):
    # 依此访问所有对象是否包含该值
    for config in self._configs:
      val = config.get(section, option, raw=raw, vars=vars, fallback=_UNSET)
      if val is not _UNSET:
        break
    if val is _UNSET and val is fallback:
      raise configparser.NoOptionError(option, section)
    return fallback if val is _UNSET else val

  def set(self, section: str, option: str, value: str = None) -> None:
    """设置值则取优先级最高的文件设置

    Args:
        section (str): 节区名字
        option (str): 选项名字
        value (str | None, optional):选项值

    Returns:
        _type_: None
    """
    ConfigParserChain.section_set_value(self._configs[0], section, option, value)

  def set_path(self, path: Path, section: str, option: str, value: str = None) -> None:
    ConfigParserChain.section_set_value(self.find_config(path, True), section, option, value)

  def find_config(self, path: Path, check=True) -> configparser.ConfigParser:
    for config in self._configs:
      if config.path == path:
        return config
    if check:
      raise ArgumentError(_('没找到指定的配置文件,如果不存在请先创建它再获取配置: {}').format(path))
    return None

  def save(self, space_around_delimiters=True):
    """保存配置到文件,还是保存到同一位置
    """
    for config in self._configs:
      ConfigParserChain.write_to_file(config, config.path, space_around_delimiters)

  def write_path(self, orig_path: Path, new_path: Path) -> None:
    """重写指定路径配置文件到新路径

    Args:
        orig_path (Path): 原始配置文件路径
        new_path (Path): 新配置文件路径
    """
    ConfigParserChain.write_to_file(self.find_config(orig_path, True), new_path)

  def write(self, fp, space_around_delimiters: bool = True) -> None:
    """重写写入函数,因为我们已经跟踪了路径,则没有必要指定另外的路径,
    如果确实需要重写它到另外的路径则调用 write_path
    """
    self.save(space_around_delimiters)

  def save_path(self, path: Path, space_around_delimiters=True):
    ConfigParserChain.write_to_file(self.find_config(path), path, space_around_delimiters)

  def remove_option(self, section: str, option: str) -> bool:
    """默认只移除最高优先级的选项
    """
    return ConfigParserChain.remove_config_option(self._configs[0], section, option)

  def remove_option_path(self, path: Path, section: str, option: str) -> bool:
    return ConfigParserChain.remove_config_option(self.find_config(path, True), section, option)

  def remove_section(self, section: str) -> bool:
    """默认只移除最高优先级的节区
    """
    return ConfigParserChain.remove_config_section(self._configs[0], section)

  def remove_section_path(self, path: Path, section: str) -> bool:
    return ConfigParserChain.remove_config_section(self.find_config(path, True), section)

  def new_section(self, section: str, allow_duplicate=True) -> str:
    conf = self._configs[0]
    if allow_duplicate or not conf.has_section(section):
      conf.add_section(section)
      return section
    # 不允许重复则要添加后缀
    suffix = 1
    name = section + '_' + str(suffix)
    while conf.has_section(name):
      suffix = suffix + 1
      name = section + '_' + str(suffix)
    conf.add_section(name)
    return section

  def __getattr__(self, name: str):
    """默认未实现的方法转发到第一个对象上
    """
    if name == '_configs':
      raise AttributeError(_('属性还未初始化: _configs'))
    if len(self._configs) > 0:
      conf = self._configs[0]
      if hasattr(conf, name) and callable(getattr(conf, name)):
        return lambda *args, **kwargs: getattr(conf, name)(*args, **kwargs)
      raise AttributeError(_('类存在未知属性: {}, 属性名: {}').format(
          type(self._configs[0]), name))
    raise AttributeError(_('未知属性: {}').format(name))


class ConfigObjectChain():
  """多个配置对象,依此获取值,支持普通对象和字典对象且对象不区分节区
  """

  @staticmethod
  def set_object_value(obj: object | dict, key: str, value: any):
    if isinstance(obj, dict):
      obj[key] = value
    else:
      setattr(obj, key, value)

  def __init__(self) -> None:
    self._objects: list[object | dict] = []

  def add_object(self, obj: object | dict):
    if obj is None:
      return
    self._objects.insert(0, obj)

  def get(self, key: str):
    val = None
    for obj in self._objects:
      if isinstance(obj, dict):
        val = obj.get(key)
      elif hasattr(obj, key):
        val = getattr(obj, key)
      if val is not None:
        return val
    return val

  def get_object(self, obj: object | dict, key: str):
    val = None
    if obj is not None:
      if isinstance(obj, dict):
        val = obj.get(key)
      elif hasattr(obj, key):
        val = getattr(obj, key)
    if val is not None:
      return val
    return self.get(key)

  def set(self, key: str, value: any):
    ConfigObjectChain.set_object_value(self._objects[0], key, value)

  def set_object(self, obj: object | dict, key: str, value: any):
    if obj is not None:
      ConfigObjectChain.set_object_value(obj, key, value)
    else:
      self.set(key, value)

  def set_active_object(self, obj: object | dict):
    """仅简单的将该对象放在列表开头,不移动对象
    """
    if obj is not None:
      self._objects.insert(0, obj)

  def remove_object(self, obj: object | dict):
    self._objects.remove(obj)


class Configurator():
  """提供一个方便的配置文件处理器,常用于参数处理操作完成后记得调用 `save` 保存配置到文件
  """

  element_types = [int, bool, str]

  def __init__(self, path: Path = utils.global_config_path,
               section: str = DEFAULTSECT,
               obj: object = None,
               file_priority=False,
               overload=True) -> None:
    """初始化一个配置管理器,与 ConfigParser 有以下不同
    1. 更多的操作数据方式,添加 list, path 等操作
    2. 提供对象模式,可以从对象和配置文件中读取配置,可以设置优先级
    3. 提供多配置文件模式,可以添加多配置文件重载设置,也支持配置文件中自定义配置重载文件
    4. 提供多对象模式,当从一个对象中获取值为 None 时可以继续从下一个对象上获取

    Args:
        path (Path, optional): 配置文件的路径. 默认值是当前用户目录下的 `.devtools.ini` 文件, 删除配置文件时默认删除它.
        section (str, optional): 当前配置操作的节区名,可以随时更换. 默认操作节区 'DEFAULT'.
        obj (object, optional): 读取配置的对象,不存在节区的区分.Defaults to None.
        file_priority(bool, optional): 配置文件优先还是对象优先.默认是对象优先
        overload(bool, optional): 重载配置文件,从 DEFAULT 节区中读取 file 配置的文件路径,如果文件存在则重载,否则还是使用自身
    """
    self._config: ConfigParserChain = ConfigParserChain()
    # 默认的配置路径没有则创建一个,否则不应该使用它
    self._config.add_config_path(path, True, overload)
    self._obj: ConfigObjectChain = ConfigObjectChain()
    self._obj.add_object(obj)
    self._path = path
    self._section: str = section
    self._file_priority = file_priority
    self.separator = ','

  def __getattr__(self, name: str) -> Any:
    """ 转发方法调用,适当的转发到 配置文件对象和配置对象上,优先转发到配置文件上
    """
    if hasattr(self._config, name) and callable(getattr(self._config, name)):
      return lambda *args, **kwargs: getattr(self._config, name)(*args, **kwargs)

    if hasattr(self._obj, name) and callable(getattr(self._obj, name)):
      return lambda *args, **kwargs: getattr(self._obj, name)(*args, **kwargs)
    raise AttributeError(_('未知属性: {}').format(name))

  @staticmethod
  def support_type(obj: Any) -> bool:
    if obj is None:
      return False
    ty = type(obj)
    if ty in Configurator.element_types:
      return True
    if isinstance(ty, list):
      for v in obj:
        if not Configurator.support_type(v):
          return False
      return True
    elif issubclass(ty, PurePath):
      return True
    return False

  def _get_activity_section(self, section: str) -> str:
    if not section:
      section = self._section
    if not section:
      section = DEFAULTSECT
    return section

  def _get_object_value(self, key: str, obj: object):
    return self._obj.get_object(obj, key)

  def _get_file_value(self, key: str, section: str):
    return self._config.get(self._get_activity_section(section), key, fallback=None)

  def _get_value(self, key: str, section: str, obj: object, fallback):
    """如果对象不为空,则对象优先,否则按照设置的优先级顺序
    """
    if self._file_priority and obj is None:
      val = self._get_file_value(key, section)
      if val is None:
        val = self._get_object_value(key, obj)
    else:
      val = self._get_object_value(key, obj)
      if val is None:
        val = self._get_file_value(key, section)
    if val is None and fallback is _UNSET:
      raise ArgumentError(_('参数不能为空: {}').format(key))
    return val if val is not None else fallback

  def set_activity_object(self, obj: object) -> None:
    self._obj.set_active_object(obj)

  def get_object_value(self, key: str) -> any:
    return self._obj.get(key)

  def get_string(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET) -> str:
    val = self._get_value(key, section, obj, fallback)
    # 回滚值可能为空
    if val:
      if isinstance(val, list):
        # 从对象上获取可能是 list
        val = self.separator.join(str(i) for i in val)
    else:
      return None
    return val

  def get_path(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET, check=False) -> Path:
    """获取文件或目录的路径

    Args:
        key (str): 选项名称
        obj (object, optional): 重载的对象
        section (str, optional): 获取的节区名称
        fallback (object, optional): 当未获取到路径时返回的默认值. Defaults to _UNSET.
        check (bool, optional): 当未设置默认值不为None时将检查获取到的路径是否存在. Defaults to True.

    Raises:
        ArgumentError: _description_

    Returns:
        _type_: _description_
    """
    val = self._get_value(key, section, obj, fallback)
    if val is None:
      return None
    path = Path(val)
    if check and not path.exists():
      raise ArgumentError(_('无效路径: {}').format(path))
    return path

  def get_path_list(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET, check=False) -> list[Path]:
    path_strings = self.get_string_list(key, obj, section, fallback)
    paths = []
    for path in path_strings:
      path = Path(path)
      if check and not path.exists():
        raise ArgumentError(_('无效路径: {}').format(path))
      paths.append(path)
    return paths

  def get_file(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET, check=False) -> Path:
    val = self.get_path(key, obj, section, fallback, check)
    if val is None:
      return None
    if check and not val.is_file():
      raise ArgumentError(_('无效文件路径: {}').format(val))
    return val

  def get_file_list(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET, check=False) -> list[Path]:
    paths = self.get_path_list(key, obj, section, fallback, check)
    if check:
      for path in paths:
        if not path.is_file():
          raise ArgumentError(_('无效文件路径: {}').format(path))
    return paths

  def get_directory(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET, check=False) -> Path:
    val = self.get_path(key, obj, section, fallback, check)
    if val is None:
      return None
    if check and not val.is_dir():
      raise ArgumentError('无效目录路径: {}'.format(val))
    return val

  def get_directory_list(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET, check=False) -> Path:
    paths = self.get_path_list(key, obj, section, fallback, check)
    if check:
      for path in paths:
        if not path.is_file():
          raise ArgumentError('无效目录路径: {}'.format(path))
    return paths

  def get_string_list(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET) -> list[str]:
    val = self.get_string(key, obj, section, fallback)
    return val.split(self.separator) if val else None

  def get_int(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET) -> int:
    val = self._get_value(key, section, obj, fallback)
    if val is None:
      return None
    # 回滚值可能是能够转换为 int 的对象
    if type(val) == str:
      return int(val)
    elif type(val) == int:
      return val
    elif type(val) == bool:
      return 1 if val else 0
    raise ArgumentError(_('期望输入类型为 int, 实际输入类型是: {}').format(type(val)))

  def get_int_list(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET) -> list[int]:
    val = self.get_string(key, obj, section, fallback)
    if val is None:
      return None

    # 回滚值不再判断list元素的值类型
    if isinstance(val, list):
      return val

    if type(val) != str:
      raise ArgumentError(_('期望输入类型为 str, 实际输入类型是: {}').format(type(val)))

    res: list[int] = list()
    for v in val.split(self.separator):
      v = v.strip().lower()
      if v == 'false' or v == 'off' or v == 'no' or v == '0':
        res.append(0)
      elif v == 'true' or v == 'on' or v == 'yes' or v == '1':
        res.append(1)
      res.append(int(v))
    return res

  def get_boolean(self, key: str, obj: object = None, section: str = None, fallback: object = _UNSET) -> bool:
    val = self._get_value(key, section, obj, fallback)
    if val is None:
      return None
    if type(val) == str:
      v = val.lower()
      if v == 'false' or v == 'off' or v == 'no' or v == '0':
        return False
      elif v == 'true' or v == 'on' or v == 'yes' or v == '1':
        return True
    elif type(val) == int:
      if val == 1:
        return True
      elif val == 0:
        return False
    elif type(val) == bool:
      return val
    raise ArgumentError(_('期望输入类型为 bool, 实际输入类型是: {}').format(type(val)))

  def get_boolean_list(self, key: str, obj: object = None, section: str = None, can_none: bool = False) -> list[bool]:
    val = self.get_string(key, obj, section, can_none)
    if val is None:
      return None

    # 不再判断回滚值中的类型
    if isinstance(val, list):
      return val

    res: list[bool] = list()
    for v in val.split(self.separator):
      v = v.lower()
      if v == 'true' or v == 'on' or v == 'yes' or v == '1':
        res.append(True)
      elif v == 'false' or v == 'off' or v == 'no' or v == '0':
        res.append(False)
      else:
        raise ArgumentError(_('无效参数({})不能转换为 bool 值: {}').format(key, v))
    return res

  def set(self, key: str, value: any, section: str = None) -> None:
    if isinstance(value, list):
      value = self.separator.join(str(i) for i in value)
    self._config.set(self._get_activity_section(section), key, value)

  def get_value_of_type(self, key: str, obj: object = None, section: str = None,
                        ty: type = str, element_type: type = str,
                        fallback: object = _UNSET) -> str | int | bool | Path | list[str | int | bool | Path]:
    val = fallback
    if ty == str:
      val = self.get_string(key, obj, section, fallback)
    elif ty == int:
      val = self.get_int(key, obj, section, fallback)
    elif ty == bool:
      val = self.get_boolean(key, obj, section, fallback)
    elif issubclass(ty, PurePath):
      val = self.get_path(key, obj, section, fallback)
    elif ty == list or ty == set:
      is_set = ty == set
      if element_type == str:
        val = self.get_string_list(key, obj, section, fallback)
      elif element_type == int:
        val = self.get_int_list(key, obj, section, fallback)
      elif element_type == bool:
        val = self.get_boolean_list(key, obj, section, fallback)
      elif issubclass(element_type, PurePath):
        val = self.get_path_list(key, obj, section, fallback)
      if is_set:
        val = set(val)
    if val is _UNSET:
      raise ArgumentError(_('不能获取配置选项: {}, 节区: {}').format(key, section))
    return val

  def update_value_from_object(self, key: str, arg: object = None, section: str = None, delete_none=False) -> None:
    """将对象中的值更新到配置文件中,自动判断类型

    Args:
        key (str): 更新的键名称
        arg (object, optional): 配置对象,如果为空则可能是做删除操作
        section (str, optional): 更新的节区
        delete_none (bool, optional): 如果值为空是否删除该节点

    Raises:
        ArgumentError: 不支持的参数类型
    """
    val = self._get_object_value(key, arg)
    if val == None:
      if delete_none:
        self.remove_item(key, section)
      return

    self.set(key, val, section)

  def remove_item(self, key: str, section: str = None) -> None:
    self._config.remove_option(self._get_activity_section(section), key)

  def remove_section(self, section: str = None) -> None:
    self._config.remove_section(self._get_activity_section(section))

  def delete_configuration(self) -> None:
    if self._path is not None and self._path.is_file():
      self._path.unlink()

  def set_activity_section(self, section: str) -> None:
    self._section = section

  def get_config(self) -> ConfigParserChain:
    return self._config

  def save(self) -> None:
    self._config.save()

  def serialization(self, obj: object):
    """序列化对象,将对象实例成员序列化到配置文件中

    Args:
        obj (object): 被实例化的对象
    """
    section = None
    for attr in vars(obj):
      # 过滤内置属性
      if attr.startswith('_') or attr.endswith('_') or attr == 'section':
        continue
      # 过滤值
      val = getattr(obj, attr)
      if not Configurator.support_type(val):
        continue
      if section is None:
        # 先获取节区名称
        section = self.new_section(obj.section, False)
      self.set(attr, val, section)

  def unserialization(self, obj: ST, section: str = None) -> None:
    """反序列化对象
    过滤以 `_` 开头或结尾的变量,即过滤内置变量和私有变量

    Args:
        obj (ST): _description_
        section (str): _description_
    """
    section = self._get_activity_section(section)
    for attr in vars(obj):
      # 过滤内置属性
      if attr.startswith('_') or attr.endswith('_'):
        continue
      if attr == 'section':
        obj.section = section
        continue
      # 过滤值
      ty0 = obj.get_variable_type(attr)
      ty1 = obj.get_list_element_type(attr) if ty0 == list or ty0 == set else None
      val = self.get_value_of_type(attr, None, section, ty0, ty1, None)
      if val is not None:
        setattr(obj, attr, val)
        obj.check_value(attr)

  def unserializations(self, ty: Type[ST]) -> list[ST]:
    ty.init_argument_information()
    objs = []
    if not issubclass(ty, aa.BaseSerialization):
      raise ArgumentError(
          _('反序列化类型必须是 `{}` 的子类').format(aa.BaseSerialization))
    for section in self._config.sections():
      obj = ty()
      self.unserialization(obj, section)
      objs.append(obj)
    return objs


def change_configure(options: argparse.Namespace):
  path: Path = options.system_file if getattr(options, 'global') else options.file
  if not options.view and path.exists() and not path.is_file():
    simple_log.error(_('输入的配置文件路径是目录而非文件: %s'), path)
    return

  def check_exist():
    if path.is_file():
      return True
    simple_log.error(_('配置文件路径不存在: %s'), path)
    return False

  if options.list:
    if check_exist():
      with path.open('r', encoding='utf-8') as f:
        print(f.read())
  elif options.delete:
    if check_exist():
      path.unlink()
      simple_log.info(_('删除配置文件成功: %s'), path)
  elif options.view:
    # 查看所有编译选项
    type: Type[ST] = getattr(options, 'view_config_option', None)
    if not type:
      simple_log.warning(_('没有配置有关配置文件选项的设置'))
      return

    args: dict[str, aa.ArgumentBean] = getattr(type, 'args', None)
    if not args:
      simple_log.error(_('类不是有效的参数配置类型,必须包含 args 静态成员: %s', type))
      return

    type.init_argument_information()

    simple_log.info(_('当前配置文件激活的节区: %s'), options.section)
    for key, bean in args.items():
      if not bean.at_config:
        continue

      name = bean.ty.__name__ if bean.ty else 'str'
      name = '{}: {}'.format(key, name)
      simple_log.info('    {: <30} # {}'.format(name, bean.tips if bean.tips else _('无选项描述信息')))
  else:
    callable = getattr(options, 'check_configure_path', None)
    if callable is not None and not callable(path, not getattr(options, 'global', False)):
      return
    # 输入的路径可能是错误的
    config = Configurator(path, options.section, overload=False)
    if options.unset:
      config.remove_item(options.key)
    elif options.unset_all:
      config.remove_section()
    else:
      config.set(options.key, options.value)
    config.save()


def add_global_config_argument(parser: argparse.ArgumentParser,
                               sub_parser: aa.SubArgumentsAction,
                               help=_('配置文件修改'),
                               global_file=utils.global_config_path,
                               local_file=Path.cwd(),
                               section='DEFAULT',
                               local_help=_('指定当前配置文件路径'),
                               hide_section=False,
                               hide_keys=[]) -> argparse.ArgumentParser:
  """为命令添加通用的配置文件处理

  配置命令是作为子命令来处理的,因此需要子命令处理器

  Args:
      parser (argparse.ArgumentParser): 命令行解析器
      sub_parser (aa.SubArgumentsAction): 要添加的子命令处理器
      help (str, optional): 子命令帮助. Defaults to '配置文件修改'.

  Returns:
      _type_: 已添加的子命令解析器,可以自定义添加参数
  """
  config_parser = sub_parser.add_parser('config', help=help)
  config_parser.add_argument('-g', '--global', help=_('使用全局配置文件'), action='store_true')

  group = config_parser.add_mutually_exclusive_group()
  group.add_argument('-l', '--list', help=_('查看配置文件'), action='store_true')
  group.add_argument('-d', '--delete', help=_('删除配置文件'), action='store_true')
  group.add_argument('--unset-all', help=_('删除当前节区的所有键'), action='store_true')

  unset_subparser: aa.SubArgumentsAction = group.add_argument('--unset', action=aa.SubArgumentsAction, help=_('删除指定键'))
  group.add_argument('-v', '--view', help=_('查看可配置的选项'), action='store_true')

  config_parser.add_argument('-f', '--file', help=local_help, default=local_file,
                             action=aa.FileAction, must_exist=False)
  config_parser.add_argument('-s', '--system_file', help=_('指定全局配置文件路径'),
                             action=aa.FileAction, default=global_file, must_exist=False)

  config_parser.add_argument('--section', help=argparse.SUPPRESS if hide_section else _('节区名字'), default=section)

  unset_subparser.set_program_name(parser)
  unset_parser = unset_subparser.add_parser('unset')
  unset_parser.add_argument('key', help=_('键名称'))

  def cond(namespace, action):
    if getattr(namespace, 'list', False):
      return False
    if getattr(namespace, 'unset', False):
      return False
    if getattr(namespace, 'delete', False):
      return False
    if getattr(namespace, 'unset_all', False):
      return False
    if getattr(namespace, 'view', False):
      return False
    for key in hide_keys:
      if getattr(namespace, key, False):
        return False
    return True

  params: aa.CondSubArgumentAction = config_parser.add_argument(
      'params', action=aa.CondSubArgumentAction, callback=cond)
  params.extend_help = True
  params.set_program_name(parser)
  params_parser = params.add_parser('params', help=_('选项帮助'))
  params_parser.add_argument('key', help=_('键名称'))
  params_parser.add_argument('value', help=_('设置要修改的值,支持str,int,bool,路径和对应的list类型,使用 `,` 分割list'))
  config_parser.set_defaults(func=change_configure)
  return config_parser
