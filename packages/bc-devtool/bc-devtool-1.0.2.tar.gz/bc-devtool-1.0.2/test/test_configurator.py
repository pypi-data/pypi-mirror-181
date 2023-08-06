# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from pathlib import Path

import pytest
from bc_devtool import arg_actions as aa
from bc_devtool import configurator

logging.basicConfig(level=logging.INFO)

AB = aa.ArgumentBean


class KeyConst():
  test_int = 'test_int'
  test_str = 'test_str'
  test_bool = 'test_bool'
  test_int_list = 'test_int_list'
  test_str_list = 'test_str_list'
  test_bool_list = 'test_bool_list'

  test_default_int = 'test_default_int'
  test_default_str_list = 'test_default_str_list'

  file = 'overload_file'
  test_section = 'test_00'

  test_object_int = 'test_object_int'
  test_file_int = 'test_file_int'


class KeyObject():
  pass


config_file_0 = {
    KeyConst.test_int: 123,
    KeyConst.test_int_list: [1, 2, 3],
    KeyConst.test_str: 'config file 0 str',
    KeyConst.test_str_list: ['config', 'file', '0', 'str'],
    KeyConst.test_bool: False,
    KeyConst.test_bool_list: [True],

    # 默认数据
    KeyConst.test_default_int: 1234,
    KeyConst.test_default_str_list: ['config', 'file', '0', 'default', 'str'],

    # 配置文件专属
    KeyConst.test_file_int: 444
}

config_file_1 = {
    KeyConst.test_int: 12345,
    KeyConst.test_default_int: 123456
}

config_object_0 = {
    KeyConst.test_int: 321,
    KeyConst.test_bool: True,
    KeyConst.test_str: 'object test string',
    KeyConst.test_int_list: [3, 2, 1],
    KeyConst.test_bool_list: [True],
    KeyConst.test_str_list: ['test', 'object', 'string'],
    KeyConst.test_default_int: 555,
    KeyConst.test_default_str_list: ['test', 'default', 'object', 'string'],
    KeyConst.test_object_int: 666
}


def init_object_value(obj: KeyObject):
  for k, v in config_object_0.items():
    setattr(obj, k, v)
  return obj


def get_increase_value(val):
  if type(val) == int:
    val = val + 1
  elif type(val) == bool:
    val = not val
  elif type(val) == str:
    val = val + ' increase'
  elif isinstance(val, list):
    # list 对象需要复制一份,避免影响原对象
    val = val.copy()
    if len(val) == 0:
      val.append(1)
    elif type(val[0]) == int:
      val.append(123)
    elif type(val[0]) == bool:
      val.append(True)
    elif type(val[0]) == str:
      val.append('increase')
    else:
      assert False, str(type(val)) + str(val) + ', 无效配置值类型'
  else:
    assert False, '无效配置值类型'
  return val


def init_increase_object(obj: object, overload: object):
  for item in dir(KeyConst):
    if item.startswith('__'):
      continue
    name = getattr(KeyConst, item)
    if type(name) != str:
      continue
    if name.find('default') >= 0:
      continue
    if hasattr(obj, name):
      setattr(overload, name, get_increase_value(getattr(obj, name)))


@pytest.fixture(scope='module')
def create_data(tmp_path_factory):
  dir: Path = tmp_path_factory.mktemp('configurator')
  file = Path(dir, 'test.ini')
  logging.info(file)
  config = configurator.Configurator(file)
  for key, value in config_file_0.items():
    config.set(key, value)
    if key.find('default') < 0:
      config.set(key, get_increase_value(value), KeyConst.test_section)

  # 添加重载数据
  overload_path = Path(dir, 'test2.ini')
  overload_config = configurator.Configurator(overload_path)
  for key, value in config_file_1.items():
    overload_config.set(key, value)
    if key.find('default') < 0:
      overload_config.set(key, get_increase_value(
          value), KeyConst.test_section)
  overload_config.save()

  config.set(KeyConst.file, overload_path, configurator.DEFAULTSECT)
  config.save()
  yield file
  overload_path.unlink()
  file.unlink()
  logging.info('删除测试文件')


@pytest.fixture(scope='module')
def create_object_data():
  normal_obj = KeyObject()
  init_object_value(normal_obj)
  overload_obj = KeyObject()
  init_increase_object(normal_obj, overload_obj)

  obj = KeyObject()
  obj.normal = normal_obj
  obj.overload = overload_obj
  return obj


@pytest.fixture(scope='module')
def create_dict_object_data():
  obj = KeyObject()
  obj.normal = config_object_0
  overload = {}

  for k, v in config_object_0.items():
    if k.find('default') < 0:
      overload[k] = get_increase_value(v)

  obj.overload = overload
  return obj


def test_base_configurator(create_data):
  """测试基本的配置文件,内部默认属性设置
  """
  config = configurator.Configurator(create_data, overload=False)
  config.set_activity_section(KeyConst.test_section)
  assert config.get_boolean(
      KeyConst.test_bool) != config_file_0[KeyConst.test_bool]
  assert config.get_string(KeyConst.test_str) == get_increase_value(
      config_file_0[KeyConst.test_str])
  assert config.get_boolean_list(KeyConst.test_bool_list) == get_increase_value(
      config_file_0[KeyConst.test_bool_list])
  assert config.get_string(KeyConst.test_str_list) == ','.join(
      get_increase_value(config_file_0[KeyConst.test_str_list]))
  assert config.get_string_list(
      KeyConst.test_str_list) != config_file_0[KeyConst.test_str_list]

  assert config.get_int(
      KeyConst.test_default_int) == config_file_0[KeyConst.test_default_int]
  assert config.get_string_list(
      KeyConst.test_default_str_list) == config_file_0[KeyConst.test_default_str_list]


def test_overload_configurator(create_data):
  """测试多个配置文件重载
  """
  config = configurator.Configurator(create_data, overload=True)
  v1 = get_increase_value(config_file_1[KeyConst.test_int])
  v2 = config.get_int(KeyConst.test_int, section=KeyConst.test_section)

  assert v1 == v2
  assert config.get_int(
      KeyConst.test_default_int) == config_file_1[KeyConst.test_default_int]
  assert config.get_int(
      KeyConst.test_int) == config_file_1[KeyConst.test_int]


def test_object(create_data, create_object_data, create_dict_object_data):
  """测试基本的对象模式
  """
  config = configurator.Configurator(
      create_data, obj=create_object_data.normal, overload=False)
  assert config.get_int(
      KeyConst.test_int) == config_object_0[KeyConst.test_int]
  assert config.get_boolean(KeyConst.test_bool, section=KeyConst.test_section) != (
      not config_object_0[KeyConst.test_bool])

  assert config.get_string(KeyConst.test_str_list) == ','.join(
      config_object_0[KeyConst.test_str_list])
  assert config.get_string_list(
      KeyConst.test_str_list) == config_object_0[KeyConst.test_str_list]

  config = configurator.Configurator(
      create_data, obj=create_dict_object_data.normal, overload=False)
  assert config.get_int(
      KeyConst.test_int) == config_object_0[KeyConst.test_int]
  assert config.get_boolean(KeyConst.test_bool, section=KeyConst.test_section) != (
      not config_object_0[KeyConst.test_bool])

  assert config.get_string(KeyConst.test_str_list) == ','.join(
      config_object_0[KeyConst.test_str_list])
  assert config.get_string_list(
      KeyConst.test_str_list) == config_object_0[KeyConst.test_str_list]


def test_overload_object(create_data, create_object_data, create_dict_object_data):
  """测试多对象重载模式
  """
  config = configurator.Configurator(
      create_data, obj=create_object_data.normal, overload=False)
  config.add_object(create_object_data.overload)

  assert config.get_int(KeyConst.test_int) == get_increase_value(
      config_object_0[KeyConst.test_int])
  assert config.get_boolean(
      KeyConst.test_bool, section=KeyConst.test_section) != config_object_0[KeyConst.test_bool]

  assert config.get_string(KeyConst.test_str_list) == ','.join(
      get_increase_value(config_object_0[KeyConst.test_str_list]))
  assert config.get_string_list(KeyConst.test_str_list, section=KeyConst.test_section) == get_increase_value(
      config_object_0[KeyConst.test_str_list])

  assert config.get_int(
      KeyConst.test_int, create_object_data.normal) == config_object_0[KeyConst.test_int]

  assert config.get_int(
      KeyConst.test_default_int) == config_object_0[KeyConst.test_default_int]
  assert config.get_string_list(
      KeyConst.test_default_str_list) == config_object_0[KeyConst.test_default_str_list]

  config = configurator.Configurator(
      create_data, obj=create_dict_object_data.normal, overload=False)
  config.add_object(create_dict_object_data.overload)

  assert config.get_int(KeyConst.test_int) == get_increase_value(
      config_object_0[KeyConst.test_int])
  assert config.get_boolean(
      KeyConst.test_bool, section=KeyConst.test_section) != config_object_0[KeyConst.test_bool]

  assert config.get_string(KeyConst.test_str_list) == ','.join(
      get_increase_value(config_object_0[KeyConst.test_str_list]))
  assert config.get_string_list(KeyConst.test_str_list, section=KeyConst.test_section) == get_increase_value(
      config_object_0[KeyConst.test_str_list])

  assert config.get_int(
      KeyConst.test_int, create_dict_object_data.normal) == config_object_0[KeyConst.test_int]

  assert config.get_int(
      KeyConst.test_default_int) == config_object_0[KeyConst.test_default_int]
  assert config.get_string_list(
      KeyConst.test_default_str_list) == config_object_0[KeyConst.test_default_str_list]


def test_config_and_object(create_data, create_object_data):
  """测试对象和配置文件一起
  """
  config = configurator.Configurator(
      create_data, obj=create_object_data.normal, overload=False, file_priority=False)
  assert config.get_boolean(
      KeyConst.test_bool, section=KeyConst.test_section) == config_object_0[KeyConst.test_bool]
  assert config.get_int(KeyConst.test_int, create_object_data.normal,
                        KeyConst.test_section) == config_object_0[KeyConst.test_int]
  assert config.get_int(
      KeyConst.test_file_int) == config_file_0[KeyConst.test_file_int]
  assert config.get_int(
      KeyConst.test_object_int) == config_object_0[KeyConst.test_object_int]

  config = configurator.Configurator(
      create_data, obj=create_object_data.normal, overload=False, file_priority=True)
  assert config.get_boolean(
      KeyConst.test_bool) == config_file_0[KeyConst.test_bool]
  assert config.get_int(KeyConst.test_int, create_object_data.normal,
                        KeyConst.test_section) == config_object_0[KeyConst.test_int]
  assert config.get_int(
      KeyConst.test_file_int) == config_file_0[KeyConst.test_file_int]
  assert config.get_int(
      KeyConst.test_object_int) == config_object_0[KeyConst.test_object_int]


def test_file(create_data):
  config = configurator.Configurator(create_data, overload=False)
  path = config.get_file(KeyConst.file, check=True)
  assert path.exists()


def test_save(tmp_path):
  path: Path = tmp_path / 'test3.ini'
  config = configurator.Configurator(path)
  config.set(KeyConst.test_int, 10)
  config.save()
  assert path.is_file()
  config.delete_configuration()
  assert not path.exists()
  config.delete_configuration()


class TestBean(aa.BaseSerialization):
  args = {
      'path': AB(ty=aa.FileAction, help='路径'),
      'from_e': AB(ty=int, help='start'),
      'section': AB(ty=str, help='name'),
      'to_e': AB(ty=str, help='目标编码')
  }

  def __init__(self):
    self.path = None
    self.from_e = ''
    self.to_e = None
    self.section = None


def test_serialization(tmp_path):
  path: Path = Path(tmp_path, 'test4.ini')
  config = configurator.Configurator(path)
  obj = TestBean()
  obj.path = path
  obj.from_e = 5
  obj.to_e = 'utf-8'
  obj.section = 'test_section'

  config.serialization(obj)

  assert config.get_int('from_e', section=obj.section) == 5
  assert config.get_string('to_e', section=obj.section) == 'utf-8'

  obj.section = 'test_section2'
  obj.from_e = 6
  config.serialization(obj)
  logging.info('section len: %s', config.sections())

  assert config.get_int('from_e', section=obj.section) == 6

  objs = config.unserializations(TestBean)
  assert len(objs) == 2

  for item in objs:
    assert item.path == path
    if item.section == 'test_section':
      assert item.from_e == 5
      assert item.to_e == 'utf-8'
    else:
      assert item.from_e == 6
  path.unlink()
