# -*- coding: utf-8 -*-
"""argparse 的各种自定义 action
"""
from __future__ import annotations

import argparse
import enum
import gettext
import inspect
import sys
from ctypes import ArgumentError
from pathlib import Path
from typing import Callable
from typing import List
from typing import Type
from typing import TypeVar

_ = gettext.translation('arg_actions', Path.joinpath(Path(__file__).parent, 'locale'), fallback=True).gettext
AT = TypeVar('AT', bound=argparse.Action)
_default = object()


def _format_action_help(action: argparse.Action):
  format = DefaultsHelpFormatter('va')
  format.add_argument(action)
  return format.format_help()


def remove_action_keys(parser: argparse.ArgumentParser, *args: list[str]):
  for key in args:
    for action in parser._actions:
      if action.dest == key:
        parser._actions.remove(action)
        break


def remove_actions(parser: argparse.ArgumentParser, *args: list[AT]):
  for arg in args:
    for action in parser._actions:
      if action == arg:
        parser._actions.remove(action)
        break


def _create_action_object(create_type,
                          option_strings,
                          dest,
                          *args,
                          **kwargs):
  registry = {}
  registry['store'] = argparse._StoreAction
  registry['store_const'] = argparse._StoreConstAction
  registry['store_true'] = argparse._StoreTrueAction
  registry['store_false'] = argparse._StoreFalseAction
  registry['append'] = argparse._AppendAction
  registry['append_const'] = argparse._AppendConstAction
  registry['count'] = argparse._CountAction
  registry['help'] = argparse._HelpAction
  registry['version'] = argparse._VersionAction
  registry['parsers'] = argparse._SubParsersAction

  if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
    registry['extend'] = argparse._ExtendAction

  if create_type is None:
    create_type = argparse._StoreAction
  elif isinstance(create_type, str):
    create_type = registry.get(create_type, None)

  if create_type is None or not isinstance(create_type, type):
    raise ArgumentError(f'unknown action type: {create_type}')

  signature = inspect.signature(create_type.__init__)
  kwargs['option_strings'] = option_strings
  kwargs['dest'] = dest
  keyword_params = dict()
  position_params = []
  kinds = [param.kind for param in signature.parameters.values()]
  has_positional_var = False
  has_var_keyword = inspect.Parameter.VAR_KEYWORD in kinds

  def _get_default_value(param):
    val = kwargs.pop(param.name, _default)
    if val is _default:
      if param.default is inspect.Parameter.empty:
        val = None
      else:
        val = param.default
    return val

  for param in signature.parameters.values():
    if param.name == 'self':
      continue
    if param.kind == inspect.Parameter.POSITIONAL_ONLY:
      position_params.append(_get_default_value(param))
    elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD or param.kind == inspect.Parameter.KEYWORD_ONLY:
      if not has_var_keyword:
        keyword_params[param.name] = _get_default_value(param)
    elif param.kind == inspect.Parameter.VAR_POSITIONAL:
      has_positional_var = True

  if has_var_keyword:
    if has_positional_var:
      action = create_type(*position_params, *args, **kwargs)
    else:
      action = create_type(*position_params, **kwargs)
  else:
    if has_positional_var:
      action = create_type(*position_params, *args, **keyword_params)
    else:
      action = create_type(*position_params, **keyword_params)
  return action


class _RequiredAction(argparse.Action):
  """条件依赖动作, 一个选项可以依赖其它多个选项,
  当选项值是字符串时,还可根据具体的字符串依赖不同参数
  """

  def __init__(self,
               option_strings,
               dest,
               actions: list[AT] = [],
               action_type=argparse._StoreAction,
               bind_value=False,
               nargs=None,
               const=None,
               default=None,
               type=None,
               choices=None,
               required=False,
               help=None,
               metavar=None,
               *args,
               **kwargs) -> None:
    self._actions: dict[str, set[AT]] = {}
    self._actions[None] = set(actions)
    self._action: argparse.Action = _create_action_object(action_type, option_strings, dest, nargs=nargs, const=const,
                                                          default=default, type=type, choices=choices, required=required,
                                                          help=help, metavar=metavar, *args, **kwargs)
    super().__init__(option_strings, dest, self._action.nargs, self._action.const,
                     self._action.default, self._action.type, self._action.choices,
                     self._action.required, self._action.help, self._action.metavar)
    # 当 bind_value 值为 True 时,根据实际参数的值来切换不同的请求项
    self._bind_value = bind_value

  def set_bind_value(self, bind: bool = True):
    self._bind_value = bind

  def add_required(self, need_value: str, *action_objs: AT) -> None:
    """添加依赖参数,当参数值与指定的 required_value 值匹配时,
    则其它依赖参数必须被赋值
    Args:
        required_value (str): 请求的参数值
    """
    need_value = need_value if self._bind_value else None
    actions = self._actions.get(need_value)
    for action in action_objs:
      if action is None:
        continue
      if actions:
        actions.add(action)
      else:
        actions = set({action})
        self._actions[need_value] = actions

  def get_required(self, need_value) -> set[AT]:
    cond = need_value if self._bind_value else None
    if isinstance(cond, list):
      actions = set()
      for c in cond:
        for e in self._actions.get(c, set()):
          actions.add(e)
      return actions
    return self._actions.get(cond, set())

  def get_requires(self):
    requires = set()
    for action in self._actions.values():
      for e in action:
        requires.add(e)
    return requires

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    self._action(parser, namespace, values, option_string)


class TrueRequiredAction(_RequiredAction):
  """条件必须参数依赖,当一个参数是满足指定值时则依赖它的其它参数都是必须参数
  唯一限制是传参时条件参数必须先指定,后才能跟依赖参数,否则后初始化无法影响之前的值
  """

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    for action in self.get_required(values):
      action.required = True
    super().__call__(parser, namespace, values, option_string)


class FalseRequiredAction(_RequiredAction):
  """条件参数排斥依赖,当该参数满足某条件时,其它 action 必须不存在
  """

  def __call__(self, parser, namespace, values, option_string=None):
    for action in self.get_required(values):
      action.required = False
    super().__call__(parser, namespace, values, option_string)


class RemoveAction(argparse.Action):
  def __init__(self,
               option_strings,
               dest,
               action_type=argparse._StoreAction,
               remove_actions: list[AT] = [],
               remove_keys: list[str] = [],
               nargs=None,
               const=None,
               default=None,
               type=None,
               choices=None,
               required=False,
               help=None,
               metavar=None,
               *args,
               **kwargs) -> None:
    self._action: argparse.Action = _create_action_object(action_type, option_strings, dest, nargs=nargs, const=const,
                                                          default=default, type=type, choices=choices, required=required,
                                                          help=help, metavar=metavar, *args, **kwargs)
    self.removes = remove_actions
    self.remove_keys = remove_keys
    super().__init__(option_strings, dest, self._action.nargs, self._action.const,
                     self._action.default, self._action.type, self._action.choices,
                     self._action.required, self._action.help, self._action.metavar)

  def add_remove_action(self, *actions: list[AT]):
    for action in actions:
      self.removes.append(action)

  def add_remove_key(self, *keys: list[str]):
    for key in keys:
      self.remove_keys.append(key)

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    self._action(parser, namespace, values, option_string)
    remove_action_keys(parser, self.remove_keys)
    remove_actions(self.removes)


class PathAction(argparse._StoreAction):
  """路径参数动作解析,保证输入的路径必须存在
  """

  def __init__(self,
               option_strings,
               dest,
               must_exist=True,
               nargs=None,
               const=None,
               default=None,
               type=None,
               choices=None,
               required=False,
               help=None,
               metavar=None,
               **kwargs) -> None:
    self._must_exist = must_exist
    super().__init__(option_strings, dest, nargs, const, default, type, choices, required, help, metavar)

  def check_value(self, value, option_string):
    path = Path(value).resolve()
    if self._must_exist and not path.exists():
      name = option_string if option_string else self.dest.upper()
      raise ValueError(_('输入无效的路径: {} {}\n参数帮助:\n\t{}').format(name, path, _format_action_help(self)))
    return path

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    if values == None or len(values) < 1:
      raise ValueError(_('输入参数不能为空: {}').format(option_string))

    # 可能是list
    if isinstance(values, list):
      paths = [self.check_value(x, option_string) for x in values]
    else:
      paths = self.check_value(values, option_string)
    setattr(namespace, self.dest, paths)


class FileAction(PathAction):
  """文件参数动作解析,保证输入的路径是有效的文件
  """

  def check_value(self, value, option_string):
    p = Path(value).resolve()

    if p.exists() and not p.is_file():
      name = option_string if option_string else self.dest.upper()
      raise ValueError(_('输入无效的文件路径: {} {}\n参数帮助:\n\t{}').format(name, p, _format_action_help(self)))

    if self._must_exist and not p.is_file():
      name = option_string if option_string else self.dest.upper()
      raise ValueError(_('输入无效的文件路径: {} {}\n参数帮助:\n\t{}').format(name, p, _format_action_help(self)))
    return p


class DirectoryAction(PathAction):
  """目录参数动作解析,保证输入的路径是有效的目录
  """

  def check_value(self, value, option_string):
    p = Path(value).resolve()
    if p.exists() and not p.is_dir():
      name = option_string if option_string else self.dest.upper()
      raise ValueError(_('输入无效的目录: {} {}\n参数帮助:\n\t{}').format(name, p, _format_action_help(self)))
    if self._must_exist and not p.is_dir():
      name = option_string if option_string else self.dest.upper()
      raise ValueError(_('输入无效的目录: {} {}\n参数帮助:\n\t{}').format(name, p, _format_action_help(self)))
    return p


class ListAction(argparse._AppendAction):
  """list[str] 参数动作解析,解析输入参数通过逗号和默认分隔符分隔参数,自动去除参数前后的空白字符,并且支持 append 参数

  Args:
      argparse (argparse.Action): 父动作是 append 类型
  """

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    super().__call__(parser, namespace, values, option_string)
    contents = []
    for value in getattr(namespace, self.dest, []):
      items = value.strip().split()
      for item in items:
        args = item.split(',')
        for v in args:
          v = v.strip()
          if len(v) > 0:
            contents.append(v)
    setattr(namespace, self.dest, contents)


class SetAction(argparse._AppendAction):
  """set[str] 参数动作解析,解析输入参数通过默认分隔符和逗号分隔,且支持 append 参数,
  虽然集合不能重复,但实际类型还是 list[str] 因为我们要做 append 操作,所以需要将 set 转换为 list

  Args:
      argparse (argparse.Action): 父动作是 append 类型
  """

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    super().__call__(parser, namespace, values, option_string)
    contents = set()
    for value in getattr(namespace, self.dest, set()):
      items = value.strip().split()
      for item in items:
        args = item.split(',')
        for v in args:
          v = v.strip()
          if len(v) > 0:
            contents.add(v)

    setattr(namespace, self.dest, list(contents))


class EnumAction(argparse.Action):
  """定义枚举类型的参数,可以设置简短的参数别名

  Args:
      argparse (_type_): 普通动作
  """

  def __init__(self,
               option_strings,
               dest,
               nargs=None,
               const=None,
               default=None,
               type=None,
               choices=None,
               required=False,
               help=None,
               metavar=None,
               **kwargs) -> None:
    enum_type = type
    default_value = default

    if enum_type is None and default_value is None:
      raise ValueError('type or default value must be assigned an Enum when using EnumAction')

    if enum_type is not None and not issubclass(enum_type, enum.Enum):
      raise TypeError('type must be an Enum when using EnumAction')

    if default_value is not None:
      if isinstance(default_value, (set, list)):
        if len(default_value) == 0:
          raise ValueError('default collection cannot be empty')
        if not all(isinstance(value, enum.Enum) for value in default_value):
          raise ValueError('default value all element must be an Enum: {}'.format(default_value))
      elif not isinstance(default_value, enum.Enum):
        raise ValueError('default value must be an Enum when using EnumAction')

    if enum_type is None:
      if isinstance(default_value, set):
        for e in default_value:
          enum_type = type(e)
          break
      elif isinstance(default_value, list):
        enum_type = type(default_value[0])
      else:
        enum_type = type(default_value)

    chios = tuple(e.name.lower() for e in enum_type)
    self._enum = enum_type
    self._short = []
    super().__init__(option_strings, dest, nargs, const, default_value, type, chios, required, help, metavar)

  def _find_enum_object(self, name: str) -> TypeVar('AE', bound=enum.Enum):
    """根据参数获取对应的枚举对象,优先查找别名参数,再查找枚举字符串参数

    Args:
        self (_type_):
        bound (enum.Enum, optional): Defaults to enum.Enum.

    Returns:
        _type_: _description_
    """
    name = name.lower()
    for e in self._enum:
      if name == e.name.lower():
        return e
    return None

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    if isinstance(values, list):
      value = [self._find_enum_object(x) for x in values]
    else:
      value = self._find_enum_object(values)
    setattr(namespace, self.dest, value)


class NestedAction(argparse.Action):
  """嵌套action, 最后一个action取决定作用,赋值时会依次调用所有子 action

  Args:
      argparse (Action): 默认父动作为空
  """

  def __init__(self,
               option_strings,
               dest,
               childs: list[Type[AT]] = [],
               nargs=None,
               const=None,
               default=None,
               type=None,
               choices=None,
               required=False,
               help=None,
               metavar=None,
               *args,
               ** kwargs) -> None:
    self._childs = []
    self._kwargs = kwargs
    super().__init__(option_strings, dest, nargs, const, default, type, choices, required, help, metavar)
    self.add_child_action(childs, *args, **kwargs)
    self._kwargs = None

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    for action in self._childs:
      if action:
        action.__call__(parser, namespace, values, option_string)

  def add_child_action(self, action_class: list[Type[AT]], *args, **kwargs) -> List[argparse.Action]:
    for item_class in action_class:
      action = _create_action_object(item_class, self.option_strings, self.dest,
                                     nargs=self.nargs, const=self.const,
                                     default=self.default, type=self.type,
                                     choices=self.choices, required=self.required,
                                     help=self.help, metavar=self.metavar, *args, **kwargs)

      self._childs.append(action)
      # 更新子选项影响的参数
      self.__dict__.update(action.__dict__)
    return self._childs

  def get_action_from_class(self, action_class: Type[AT]) -> AT:
    for action in self._childs:
      if type(action) == action_class:
        return action
    return None

  def get_actions(self):
    return self._childs


class StoreTrueAction(argparse._StoreConstAction):
  """与 argparse 模块不同的是它的默认值是 None
  """

  def __init__(self,
               option_strings,
               dest,
               default=None,
               required=False,
               help=None):
    super().__init__(
        option_strings=option_strings,
        dest=dest,
        const=True,
        default=default,
        required=required,
        help=help)


class StoreFalseAction(argparse._StoreConstAction):
  """与 argparse 模块不同的是它的默认值是 None
  """

  def __init__(self,
               option_strings,
               dest,
               default=None,
               required=False,
               help=None):
    super().__init__(
        option_strings=option_strings,
        dest=dest,
        const=True,
        default=default,
        required=required,
        help=help)


class IntMaxMinAction(argparse._StoreAction):
  """限制了输入 int 参数的最大和最小值[min, max]
  """

  def __init__(self, option_strings,
               dest,
               min=0,
               max=100,
               nargs=None,
               const=None,
               default=None,
               type=None,
               choices=None,
               required=False,
               help=None,
               metavar=None,
               **kwargs) -> None:
    self.min = min
    self.max = max
    super().__init__(option_strings, dest, nargs, const, default, int, choices, required, help, metavar)

  def __call__(self, parser, namespace, values, option_string=None) -> None:
    super().__call__(parser, namespace, values, option_string)
    v = getattr(namespace, self.dest)
    if v < self.min or v > self.max:
      raise ValueError(_('输入参数(`{}`)范围错误, 期望范围: {} ~ {}, 实际输入: {}').format(option_string, self.min, self.max, v))


class SubArgumentsAction(argparse._SubParsersAction):
  """子命令参数解析器,与 argparse._SubParsersAction 不同,它是可选的

  1. 第一次调用 `add_parser` 添加的解析器是默认的解析器,当参数未指定时自动使用默认解析器
  2. 通常内部只添加一个子解析器,如果要添加多个子解析器则在处理帮助信息时需要额外处理,如用
  它替换自带的 `argparse.add_subparsers` 来做参数处理
  3. 当 parse_help 为 True 时作为顶级子命令解析器处理,例如包含 action1 默认子解析器时
    parse_help = False 时 python arg_actions.py -h 则实际输出的是 python arg_actions.py action1 -h
    parse_help = True 时 python arg_actions.py -h 才实际输出对应帮助信息
    同时在打印帮助信息时 parse_help = False 会省略 action1 的输出
  4. extend_help 为 True 时则在打印帮助信息时会展开参数到上一级命令,它的帮助信息就该为 None
  Args:
      argparse (_type_): _description_
  """

  def __init__(self, option_strings, prog='SubArgument', parser_class=argparse.ArgumentParser, dest=argparse.SUPPRESS,
               required=False, help=None, metavar=None, parse_help=False, extend_help=False):
    super().__init__(option_strings, prog, parser_class, dest, required=required, help=help, metavar=metavar)
    # 这里需要更改子参数的参数数量,因为我们不再需要传递一个子选项值,但实际可以传递,如果未传递则使用默认值
    self.nargs = argparse.REMAINDER
    self._default_parse_name = None
    self._parse_help = parse_help
    self.extend_help = extend_help

  def set_program_name(self, parser: argparse.ArgumentParser):
    """设置调用程序的名称
    因为在创建类时,本 action 还未添加到解析器中,因此无法获取上级参数
    所以需要单独调用来解析程序名称

    Args:
        parser (argparse.ArgumentParser): 父解析器
    """

    formatter = parser._get_formatter()
    positionals = []
    groups = parser._mutually_exclusive_groups
    formatter.add_usage(parser.usage, positionals, groups, '')
    prog = formatter.format_help().strip()
    stack = []

    def parse_argument_parser(child_parser: argparse.ArgumentParser) -> bool:
      for action in child_parser._actions:
        if action is self:
          # 找到了参数
          return True
        elif isinstance(action, argparse._SubParsersAction):
          # 这里要递归处理子解析器获取参数
          for key, value in action.choices.items():
            stack.append(key)
            if parse_argument_parser(value):
              return True
            stack.pop()
      return False

    if parse_argument_parser(parser):
      # 找到了
      name = ''
      if self.option_strings:
        name = '|'.join(self.option_strings)
      if stack:
        prog += ' ' + ' '.join(stack)
      if name:
        prog += ' ' + name
      self._prog_prefix = prog
    else:
      positionals = parser._get_optional_actions()
      formatter = parser._get_formatter()
      formatter.add_usage(parser.usage, positionals, groups, '')
      self._prog_prefix = formatter.format_help().strip()

  def __call__(self, parser: argparse.ArgumentParser,
               namespace: argparse.Namespace,
               values: list[str] | None,
               option_string: str | None = ...) -> None:
    if values:
      parser_name = values[0]
      if self._parse_help and (parser_name == '-h' or parser_name == '--help'):
        pass
      else:
        # 如果第一个参数不是解析器名字,则我们添加默认解析器
        try:
          parser = self._name_parser_map[parser_name]
        except KeyError:
          values.insert(0, self._default_parse_name)
    else:
      values = [self._default_parse_name]
    if self.dest:
      setattr(namespace, self.dest, True)
    return super().__call__(parser, namespace, values, option_string)

  def get_default_parser(self) -> argparse.ArgumentParser:
    return self._name_parser_map[self._default_parse_name]

  def add_parser(self, name: str, **kwargs) -> argparse.ArgumentParser:
    """添加一个子解析器,当指定 help 时会生成一项帮助参数,对应非顶级子命令解析器帮助信息
    重复,因此需按情况指定

    Args:
        name (str): 子解析器名字

    Returns:
        argparse.ArgumentParser: 生成的新子解析器
    """
    formatter_class = kwargs.pop('formatter_class', DefaultsHelpFormatter)
    prog = kwargs.pop('prog', None)
    if prog is None:
      prog = '%s %s' % (self._prog_prefix, name) if self._parse_help else self._prog_prefix

    if self.extend_help:
      kwargs.pop('help', None)
    parser = super().add_parser(name, formatter_class=formatter_class, prog=prog, **kwargs)
    # 第一个添加的解析器是默认解析器
    if self.extend_help and len(self._choices_actions) > 0:
      # 为伪action添加标志,后续格式化处理
      self._choices_actions[-1].extend_help = True
    if self._default_parse_name is None:
      self._default_parse_name = name
    return parser


class CondSubArgumentAction(SubArgumentsAction):
  def __init__(self, option_strings, prog='SubArgument', parser_class=argparse.ArgumentParser, dest=argparse.SUPPRESS,
               required=False, help=None, metavar=None, parse_help=False, extend_help=False,
               callback: Callable[[argparse.Namespace, argparse.Action], bool] = None):
    if callback is None:
      raise ArgumentError(_('条件子命令参数必须指定一个可回调的参数处理函数 callback 不能为空'))
    self.callback = callback
    super().__init__(option_strings, prog, parser_class, dest, required, help, metavar, parse_help, extend_help)

  def __call__(self, parser: argparse.ArgumentParser,
               namespace: argparse.Namespace,
               values: list[str] | None,
               option_string: str | None = ...) -> None:
    if self.callback(namespace, self):
      return super().__call__(parser, namespace, values, option_string)


class CondArgumentAction(argparse._StoreAction):
  def __init__(self,
               option_strings,
               dest,
               nargs=None,
               const=None,
               default=None,
               type=None,
               choices=None,
               required=False,
               help=None,
               metavar=None, callback: Callable[[argparse.Namespace, argparse.Action], bool] = None) -> None:
    if type is None:
      type = str
    if callback is None:
      raise ArgumentError(_('条件参数必须指定一个可回调的参数处理函数 callback 不能为空'))
    self.callback = callback
    super().__init__(option_strings, dest, nargs, const, default, type, choices, required, help, metavar)
    self.nargs = argparse.PARSER

  def __call__(self, parser, namespace, values, option_string: str | None = ...) -> None:
    if self.callback(namespace, option_string):
      return super().__call__(parser, namespace, values[0], option_string)


class TopSubArgumentsAction(SubArgumentsAction):
  """处理顶级子命令

  Args:
      SubArgumentsAction (_type_): _description_
  """

  def __init__(self, option_strings, prog='SubArgument', parser_class=argparse.ArgumentParser,
               dest=argparse.SUPPRESS, required=False, help=None, metavar=None, extend_help=False):
    super().__init__(option_strings, prog, parser_class, dest, required, help, metavar, True, extend_help)


class ArgumentEnum(enum.Enum):
  """作为参数的枚举时, 默认输出字符串是: 类名.成员名,更改为 成员名
  """

  def __str__(self):
    return '%s' % (self._name_)


class ArgumentNameEnum(ArgumentEnum):
  """获取枚举值时取 枚举对象.name
  """
  pass


class ArgumentValueEnum(ArgumentEnum):
  """获取枚举值时取 枚举对象.value, 如果 value 是列表则默认取第一个元素
  """
  pass


class DefaultsHelpFormatter(argparse.HelpFormatter):
  """与 argparse.ArgumentDefaultsHelpFormatter 以下不同点:
  1. 如果参数默认值是 None 则不添加帮助文档
  2. 添加 bool 类型说明
  3. 自定义 Action 的类型说明
  """

  @staticmethod
  def _get_actions_help(actions: list[AT]):
    help = set()
    for action in actions:
      opt = ''
      if action.option_strings is not None:
        if isinstance(action.option_strings, list):
          # 有多个选项名称则取最大名称
          for option in action.option_strings:
            if len(option) > len(opt):
              opt = option
        else:
          opt = action.option_strings

      if len(opt) == 0:
        opt = action.dest
      help.add(opt)
    return help

  def _get_nested_help_string(self, action: NestedAction):
    actions = []
    for a in action.get_actions():
      if isinstance(a, _RequiredAction):
        actions.extend(a.get_requires())
    if len(actions) == 0:
      return ''
    return _('(在指定参数之前,依赖其它参数必须被指定: {})').format(DefaultsHelpFormatter._get_actions_help(actions))

  def _get_sub_arguments_help_string(self, action: SubArgumentsAction):
    return ''

  def _get_required_help_string(self, action: _RequiredAction):
    actions = action.get_requires()
    if len(actions) == 0:
      return ''
    return _('(在指定参数之前,依赖其它参数必须被指定: {})').format(DefaultsHelpFormatter._get_actions_help(actions))

  def _get_help_string(self, action):
    help = action.help
    if isinstance(action, NestedAction):
      help += self._get_nested_help_string(action)
    if isinstance(action, _RequiredAction):
      help += self._get_required_help_string(action)
    if isinstance(action, SubArgumentsAction):
      help += self._get_sub_arguments_help_string(action)

    if '%(default)' not in action.help:
      if action.default is not argparse.SUPPRESS and action.default is not None:
        defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
        if action.option_strings or action.nargs in defaulting_nargs:
          help += ' (default: %(default)s)'
    return help

  def _format_action_invocation(self, action: argparse.Action) -> str:
    """因为 bool 类型它的 nargs = 0 所有在获取 metavar 时为空,这里单独处理

    Args:
        action (argparse.Action): 参数对应的 Action

    Returns:
        str: 描述参数的元数据
    """
    if isinstance(action, (argparse._StoreFalseAction, argparse._StoreTrueAction, StoreTrueAction, StoreFalseAction)):
      return '%s BOOL' % ', '.join(action.option_strings)
    if action.option_strings and len(action.option_strings) > 1:
      parts = []
      if action.nargs == 0:
        parts.extend(action.option_strings)
      else:
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        last = action.option_strings[-1]
        for option_string in action.option_strings:
          if last is option_string:
            parts.append('%s %s' % (option_string, args_string))
          else:
            parts.append(option_string)
      return ', '.join(parts)
    return super()._format_action_invocation(action)

  def _get_action_default_metavar(self, action):
    ty = type(action)
    if issubclass(ty, FileAction):
      return 'FILE'
    if issubclass(ty, DirectoryAction):
      return 'DIR'
    if issubclass(ty, PathAction):
      return 'PATH'
    if issubclass(ty, ListAction) or issubclass(ty, SetAction):
      return 'LIST'
    if action.type is not None:
      return action.type.__name__.upper()
    return None

  def _get_default_metavar_for_optional(self, action):
    v = self._get_action_default_metavar(action)
    if v is not None:
      return v
    return super()._get_default_metavar_for_optional(action)

  def _format_args(self, action: argparse.Action, default_metavar: str) -> str:
    if isinstance(action, SubArgumentsAction) and action.extend_help:
      return default_metavar
    return super()._format_args(action, default_metavar)

  def _metavar_formatter(self, action: argparse.Action, default_metavar: str) -> Callable[[int], tuple[str, ...]]:
    if getattr(action, 'extend_help', False):
      def format(tuple_size):
        if isinstance(default_metavar, tuple):
          return default_metavar
        else:
          return (default_metavar, ) * tuple_size
      return format
    return super()._metavar_formatter(action, default_metavar)

  def _get_expand_subargument_usage(self, parser: argparse.ArgumentParser) -> str:
    optionals = []
    positionals = []
    for action in parser._actions:
      if action.option_strings:
        if '-h' not in action.option_strings and '--help' not in action.option_strings:
          optionals.append(action)
      else:
        positionals.append(action)

    action_usage = self._format_actions_usage(
        optionals + positionals, parser._mutually_exclusive_groups)
    return action_usage

  def _get_expand_subargument_action(self, parser: argparse.ArgumentParser) -> str:
    formatter = parser._get_formatter()
    formatter._current_indent = self._indent_increment
    formatter.add_arguments(parser._positionals._group_actions)
    s = formatter.format_help()
    # 因为第一个元素会自动添加缩进,而后面的元素却没有,因此手动加上
    s = s.replace('\n', '\n' + ' ' * self._current_indent, s.count('\n')-1)
    return s

  def _get_default_metavar_for_subargument_positional(self, action: SubArgumentsAction) -> str:
    caller = sys._getframe(2).f_code.co_name
    is_usage = caller.find('usage') >= 0
    if action.extend_help:
      parser = action.get_default_parser()
      if is_usage:
        return self._get_expand_subargument_usage(parser)
      else:
        return self._get_expand_subargument_action(parser)
    return None

  def _get_default_metavar_for_positional(self, action):
    value = ''
    if isinstance(action, SubArgumentsAction):
      value = self._get_default_metavar_for_subargument_positional(action)
    elif getattr(action, 'extend_help', False):
      return ''
    if value:
      return value
    v = self._get_action_default_metavar(action)
    if v is not None:
      caller = sys._getframe(1).f_code.co_name
      if caller.find('usage') < 0:
        return action.dest.upper() + ' ' + v
    return super()._get_default_metavar_for_optional(action)


SHORT_SUPPRESS = '==SUPPRESS=='


class ArgumentBean():

  def __init__(self, short_key: str = SHORT_SUPPRESS, ty: Type = None, help: str = None,
               tips: str = None, must_exist: bool = False, element_ty: Type = str,
               long_key: str = None, positional: bool = False, set=False, at_config: bool = False, **kwargs):
    """创建参数描述对象

    Args:
        short_key (str, optional): 短参数名称, 自动添加前缀 `-`, 位置参数不使用, 不指定则默认 None
        ty (_type_, optional): 参数类型,序列化和反序列化使用. 默认是 str.
        help (str, optional): 参数的帮助文档,命令行描述. 默认是 None.
        tips (str, optional): 参数写入配置文件的帮助描述. 默认是 help 描述.
        element_ty (_type_, optional): 当参数是 list 类型时指定元素类型. 默认是 str.
        must_exist (bool, optional): 当参数是路径/文件/目录时是否确保路径必须存在. 默认是 false
        long_key (str, optional): 长参数名称,自动添加前缀 `--`,不指定则默认从键名称获取
        positional (str, optional): 位置参数,默认是可选参数

    Returns:
        _type_: _
    """
    self.short_key = short_key
    self.ty = ty
    self.help = help
    self.tips = tips if tips else help
    self.must_exist = must_exist
    self.element_ty = element_ty
    self.long_key = long_key
    self.positional = positional
    self.set = set
    self.at_config = at_config

    # 以下参数是传递给 argparse的
    self._items = []
    self._extras = kwargs


class BaseSerialization():
  """对象可以序列化与反序列化,序列化是指可以在配置文件中配置
  并恢复对应的类型和执行参数检测

  类变量存在以下字典,因为我们可能添加到参数列表中,所以为了方便
  直接使用 ArgumentBean 类型

  不允许值的类型发生改变,否则影响序列化与反序列化
  args = {
    'name': arg_actions.ArgumentBean()
  }
  """

  def get_variable_type(self, name: str) -> type:
    args = getattr(type(self), 'args', dict())
    bean = args.get(name, None)
    if isinstance(bean, ArgumentBean) and isinstance(bean.ty, type):
      return bean.ty
    return str

  def get_list_element_type(self, name: str) -> type:
    args = getattr(type(self), 'args', dict())
    bean = args.get(name, None)
    if isinstance(bean, ArgumentBean) and isinstance(bean.element_ty, type):
      return bean.element_ty
    return str

  @classmethod
  def init_argument_information(cls, obj=None):
    """在这里解析值的类型和对应的参数类型,一次解析后不再解析
    """
    init = getattr(cls, '_init_args', False)
    if init:
      return
    setattr(cls, '_init_args', True)

    # 需要一个实例对象来猜测类型
    if obj is None:
      obj = cls.get_default_singleton()

    args = getattr(cls, 'args', dict())
    # 初始化与参数有关的属性
    init_argument_information(args, obj)

  def init_default_value(self):
    pass

  @classmethod
  def get_default_singleton(cls):
    """获取静态单一实例对象,如果没有则会创建它,
    它会调用 `init_default_value` 方法初始化默认参数,
    用于有时需要默认参数而有时完全不需要默认参数,则没有必要每次
    实例化都要初始化默认参数一次

    Returns:
        _type_: _description_
    """
    val = getattr(cls, '_singleton', None)
    if val is None:
      val = cls()
      val.init_default_value()
      setattr(cls, '_singleton', val)
    return val

  def check_value(self, name: str) -> None:
    """当生成路径时需要检测它是否存在

    Args:
        name (str): 变量名称
    """
    val = getattr(self, name, None)
    # 空值不检查
    if not val:
      return
    args = getattr(type(self), 'args', dict())
    bean = args.get(name, None)
    if not isinstance(bean, ArgumentBean):
      return
    if (isinstance(bean.ty, type) and issubclass(bean.ty, PathAction)):
      val: Path = val
      if issubclass(bean.ty, FileAction):
        if val.exists() and not val.is_file():
          raise ValueError(_('值是无效的文件路径: {} = {}').format(name, val))
        if bean.must_exist and not val.is_file():
          raise ValueError(_('文件路径不存在: {} = {}').format(name, val))
      elif issubclass(bean.ty, DirectoryAction):
        if val.exists() and not val.is_dir():
          raise ValueError(_('值是无效的目录: {} = {}').format(name, val))
        if bean.must_exist and not val.is_dir():
          raise ValueError(_('目录路径不存在: {} = {}').format(name, val))
      elif issubclass(bean.ty, PathAction):
        if bean.must_exist and not val.exists():
          raise ValueError(_('路径不存在: {} = {}').format(name, val))

  def check_object_value(self) -> None:
    pass


ST = TypeVar('ST', bound=BaseSerialization)


def add_default_subparse_value(parse: argparse.ArgumentParser,
                               default_value: str,
                               args=None,
                               overload_sys_args: bool = True) -> list[str]:
  """为子解析器添加默认的选项,不处理子解析器中嵌套解析器,
  如果要嵌套处理则获取子解析器中的 解析器 再次调用即可
  只支持在命令行开头指定位置参数,可以包含其它位置参数,但他们的参数数量都该为1,否则不好区分位置参数

  需要在调用 parse.parse_args() 之前调用才生效
  Args:
      parse (argparse.ArgumentParser): 处理的解析器
      args (_type_, optional): 传入的参数. 默认为空则读取程序参数
  """
  args = sys.argv[1:] if args is None else list(args)

  positionals = parse._get_positional_actions()
  if len(positionals) == 0:
    return args

  index = 0
  nargs = len(args)
  for action in positionals:
    if isinstance(action, argparse._SubParsersAction):
      # 发现了子命令参数,则需要比较该处参数是否匹配
      try:
        if nargs < index:
          # 参数数量不满足位置参数的长度要求
          pass
        elif nargs == index:
          # 参数数量刚好差一个子命令参数,因此直接添加一个默认值
          args.append(default_value)
        else:
          parse._check_value(action, args[index])
      except argparse.ArgumentError:
        args.insert(index, default_value)
      break
    else:
      index = index + 1

  if overload_sys_args:
    args.insert(0, sys.argv[0])
    sys.argv = args
  return args


def action_to_value_type(ty: Type | str) -> Type:
  if issubclass(ty, PathAction):
    return Path
  if issubclass(ty, StoreTrueAction) or issubclass(ty, StoreFalseAction) or issubclass(ty, argparse.BooleanOptionalAction):
    return bool
  if issubclass(ty, SetAction):
    return set
  if issubclass(ty, argparse._AppendAction):
    return list
  if issubclass(ty, EnumAction):
    return enum
  if issubclass(ty, IntMaxMinAction) or issubclass(ty, argparse._CountAction):
    return int

  if isinstance(ty, str):
    if ty == 'store_true' or ty == 'store_false':
      return bool
    if ty == 'append' or ty == 'append_const':
      return list
    if ty == 'store':
      return str
    if ty == 'count':
      return int
    if ty == 'extend':
      return list
  return None


def value_to_argument_action_type(default_value: object) -> Type | str | None:
  if isinstance(default_value, Path):
    if default_value.is_dir():
      return DirectoryAction
    elif default_value.is_file() or default_value.name.find('.') >= 1:
      return FileAction
    else:
      return PathAction
  elif isinstance(default_value, bool):
    if default_value:
      return argparse.BooleanOptionalAction
    else:
      return argparse._StoreTrueAction
  elif isinstance(default_value, list):
    # list参数都作为字符串,由 逗号 分隔
    return ListAction
  return None


def init_argument_information(args: dict[str, ArgumentBean], obj: object):
  """解析参数和 action 类型

  Args:
      args (dict[str, ArgumentBean]): 类包含的参数集合
      obj (object): 提供默认值的对象
  """

  for key, bean in args.items():
    if not bean.positional:
      short = key[0] if bean.short_key is SHORT_SUPPRESS else bean.short_key
      if short:
        short = '-' + short.replace('_', '-') if short else None
        bean._items.append(short)

    long_name = bean.long_key.replace('_', '-') if bean.long_key else key.replace('_', '-')
    if not bean.positional:
      long_name = '--' + long_name
    bean._items.append(long_name)

    if bean.help:
      bean._extras['help'] = bean.help

    default_value = getattr(obj, key, None)
    has_handle_default = False
    if bean.ty:
      if issubclass(bean.ty, argparse.Action):
        bean._extras['action'] = bean.ty
        if issubclass(bean.ty, PathAction):
          bean._extras['must_exist'] = bean.must_exist

        # 将 action 转为 实际的类型
        ty = action_to_value_type(bean.ty)
        if ty:
          bean.ty = ty
      elif bean.ty is bool:
        # 如果有默认值则使用 argparse 的类,否则使用自定义类
        if default_value is None:
          bean._extras['action'] = StoreTrueAction
        elif default_value:
          bean._extras['action'] = argparse.BooleanOptionalAction
          bean._extras['default'] = True
        else:
          bean._extras['action'] = 'store_true'
        has_handle_default = True
      else:
        bean._extras['type'] = bean.ty
    elif default_value is not None:
      # 根据当前值类型猜测参数类型
      action = value_to_argument_action_type(default_value)
      if action:
        bean._extras['action'] = action
        if isinstance(action, type):
          if issubclass(action, PathAction):
            bean._extras['must_exist'] = bean.must_exist
          elif issubclass(action, ListAction):
            if bean.set:
              bean._extras['action'] = SetAction
          elif action in [argparse._StoreFalseAction, argparse._StoreTrueAction, argparse.BooleanOptionalAction, StoreTrueAction, StoreFalseAction]:
            pass
      else:
        bean._extras['type'] = type(default_value)
      bean.ty = type(default_value)

    if not has_handle_default and default_value is not None:
      bean._extras['default'] = default_value


def add_object_to_argument(parser: argparse.ArgumentParser, obj: ST | Type[ST]):
  if isinstance(obj, BaseSerialization):
    obj.init_argument_information(obj)
  else:
    obj = obj.get_default_singleton()
    obj.init_argument_information(obj)

  args: dict[str, ArgumentBean] = getattr(type(obj), 'args', dict)
  for key, bean in args.items():
    parser.add_argument(*bean._items, **bean._extras)
