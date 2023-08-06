# -*- coding: utf-8 -*-
# /usr/bin/python3
from __future__ import annotations

import codecs
import gettext
import logging
import os
import sys
from enum import auto
from enum import Enum
from enum import unique
from pathlib import Path
from typing import Callable
from typing import List

import chardet


_ = gettext.translation('arg_actions', Path.joinpath(Path(__file__).parent, 'locale'), fallback=True).gettext


def read_file_to_lines(path: Path, strip: bool = True, callback: Callable[[str], str] = None,
                       filter_line: Callable[[str], bool] = None, encoding: str = 'utf-8') -> List[str]:
  """提供多种方式读取文件内容

  Args:
      path (str): 文件路径
      strip (bool, optional): 是否执行 行内容strip. 默认值为 True.
      callback (Callable[[str], str], optional): 自定义回调修改行内容. 默认值为 None.
      filter_line (Callable[[str], bool], optional): 自定义过滤行,回调返回 True 则丢弃该行内容. 默认值为 None.
      encoding (str, optional): 读取文件的编码方式. 默认编码为 'utf-8'.

  Raises:
      FileNotFoundError: 文件未找到则抛出异常
  Returns:
      List[str]: 读取的内容集合
  """

  f = path.open(encoding=encoding)
  if f == None:
    raise FileNotFoundError(str(path))

  lines = f.readlines()
  f.close()

  if not strip and not callback and not filter_line:
    return lines

  new_contents = []
  for line in lines:
    if strip:
      line = line.strip()
    if callback:
      line = callback(line)
    if filter_line:
      if filter_line(line):
        continue
    new_contents.append(line)
  return new_contents


def visit_file_line(path: Path, callback: Callable[[str], None], encoding: str = 'utf-8'):
  """读取文件的每一行内容,并回调指定方法

  Args:
      path (str): 文件路径
      callback (Callable[[str], None]): 回调函数处理行内容
      encoding(str): 文件编码

  Raises:
      FileNotFoundError: 文件未找到则抛出异常
  """

  f = path.open(encoding=encoding)
  if not f:
    raise FileNotFoundError(path)
  for line in f.readlines():
    callback(line)
  f.close()


def _merge_multiple_text_files(files: list[Path], out, append):
  mode = 'a' if append else 'w'
  with open(out, mode) as f:
    for file in files:
      for line in file.open(encoding='utf-8'):
        f.write(line)


def _merge_multiple_bin_files(files: list[Path], out, append):
  mode = 'ab' if append else 'wb'
  with open(out, mode) as f:
    for file in files:
      with file.open('rb') as cf:
        f.write(cf.read())


def merge_multiple_files(files: list[Path], out: str, bin: bool = False, append: bool = False) -> None:
  """合并多个文件为一个文件,包含二进制模式和文本模式

  Args:
      files (list[str]): 文件路径集合
      out (str): 输出文件路径
      bin (bool, optional): 二进制合并. 默认: False.
      append (bool, optional): 追加模式. 默认: False.
  """
  if not bin:
    _merge_multiple_text_files(files, out, append)
  else:
    _merge_multiple_bin_files(files, out, append)


def make_sure_file_path(input: str | Path) -> None:
  """输入文件路径确保上级目录存在

  Args:
      input (str): 文件路径

  """
  path = Path(input).parent.resolve()
  try:
    if not path.is_dir():
      os.makedirs(str(path))
  except Exception:
    pass


def is_contains_chinese(strs: str) -> bool:
  for c in strs:
    if '\u4e00' <= c <= '\u9fff':
      return True
  return False


def get_file_encoding(path: Path) -> dict:
  raw = open(path, 'rb').read()
  result = chardet.detect(raw)
  return result


def get_binary_encoding(raw: bytes) -> dict:
  return chardet.detect(raw)


@unique
class FileConverterState(Enum):
  failed = auto()
  exception = auto()
  unchanged = auto()
  changed = auto()


class FileConverterResult():
  def __init__(self, reson: str = '') -> None:
    self.state = FileConverterState.unchanged
    self.reson = reson
    self.info = ''

  def failed(self) -> FileConverterResult:
    self.state = FileConverterState.failed
    return self

  def is_failed(self) -> bool:
    return self.state != FileConverterState.changed and self.state != FileConverterState.unchanged

  def exception_occurs(self) -> FileConverterResult:
    self.state = FileConverterState.exception
    return self

  def has_exception(self) -> bool:
    return self.state == FileConverterState.exception

  def unchanged(self) -> FileConverterResult:
    # 因为是动作集合,只要有一个改变了文件则它就是被改变的
    if self.state != FileConverterState.changed:
      self.state = FileConverterState.unchanged
    return self

  def changed(self) -> FileConverterResult:
    self.state = FileConverterState.changed
    return self

  def has_changed(self) -> FileConverterResult:
    return self.state == FileConverterState.changed

  def failed_reson(self, reson: str) -> FileConverterResult:
    self.reson = reson
    return self

  def add_info(self, info: str) -> FileConverterResult:
    self.info = info
    return self


class FileConverterCallback():
  """当执行一些转换操作时回调,只回调被转换或被检测不通过的文件
  """

  def transform_encoding(self, input: Path, output: Path, from_encoding: str, to_encoding: str):
    """编码发送转换时回调 pass

    Args:
        input (Path): 输入文件路径
        output (Path): 输出文件路径
        from_encoding (str): 输入编码
        to_encoding (str): 输出编码
    """
    pass

  def replace_content(self, input: Path, output: Path, before: bytes, after: bytes):
    """内容发生替换回调 pass

    Args:
        input (Path): 输入文件路径
        output (Path): 输出文件路径
        before (bytes): 替换之前的字节数组
        after (bytes): 替换之后的字节数组
    """
    pass

  def transform_chinese(self, input: Path, output: Path, from_encoding: str, to_encoding: str):
    """检测到中文后执行编码转换时回调

    Args:
        input (Path): 输入文件路径
        output (Path): 输出文件路径
        from_encoding (str): 输入编码
        to_encoding (str): 输出编码
    """
    pass

  def check_encoding(self, input: Path, output: Path, from_encoding: str, to_encoding: str):
    """检测编码不匹配回调 pass

    Args:
        input (Path): 输入文件路径
        output (Path): 输出文件路径
        from_encoding (str): 检测到的实际编码
        to_encoding (str): 期望的编码
    """
    pass

  def action_executed(self, input: Path, output: Path, result: FileConverterResult) -> bool:
    """每成功执行完一个动作时回调,不包含开头和结尾的读写动作,如果执行不成功则所有动作都结束

    Args:
        input (Path): 输入文件路径
        output (Path): 输出文件路径
        result (FileConverterResult): 动作执行结果包含操作失败和操作提示信息
    Returns:
        bool: 返回 True 则继续执行后续动作,否则不再继续
    """
    return True


class FileConvertAction(Enum):
  """文件转换动作,包含编码转换,内容替换等等
  """

  # 转换文件编码
  transform_encoding = auto()
  # 当文件包含中文时执行转码
  chinese_transform_encoding = auto()
  # 仅检测编码
  check_encoding = auto()
  # 替换文件内容
  replace_content = auto()
  # 转换 CRLF 换行为 LF 换行
  crlf_to_lf = auto()
  # 转换 LF 换行为 CRLF 换行
  lf_to_crlf = auto()


class FileConverter():
  """文件转换器,执行各种编码转换和内容替换
  """

  def __init__(self, input: Path, from_encoding: str = None, to_encoding: str = None, out: Path | None = None,
               confidence: float = 0.9, no_change_copy_file: bool = False, callback: FileConverterCallback = None) -> None:
    """文件编码转换,字符替换等等

    Args:
        input (str): 输入文件路径
        from_encoding (str, optional): 输入文件编码,默认为None 需要转换编码时会自动识别.
        to_encoding (str, optional): 输出文件编码, 默认为None则与输入编码一致.
        out (str, optional): 输出文件路径,默认为None,则输出路径与原路径相同.
        confidence (float, optional): 编码识别的精确度限制,如果低于该精确度则不做操作,默认限制0.9.
        no_change_copy_file (bool, optional): 当内容未发送改变时是否需要复制文件到输出路径,默认不复制.
        callback (FileConverterCallback, optional): 转换器回调对象,当执行转换时回调操作的文件,默认无回调.
    """
    self.input: Path = input
    self.from_encoding = from_encoding
    self.to_encoding = to_encoding
    self.output = out
    self.no_change_copy_file = no_change_copy_file
    self.callback = callback if callback else FileConverterCallback()

    self._confidence = confidence
    self._actions = []
    self._out_action = []
    self._from_replaces: List[bytes] = []
    self._to_replaces: List[bytes] = []
    self._repalce_index = 0
    # action 提前终止原因,后续action不再执行
    self._abort_reson: str = ''

    # 内容应该始终是 bytes 类型在多个 action 之间传递
    self._content: bytes = None
    self._changed = False
    self._guessed = False

  def _get_output(self):
    if self.output is None:
      self.output = self.input
    return self.output

  def set_confidence_limit(self, limit: float) -> None:
    """设置编码猜测限制比重,如果低于该比重则不处理

    Args:
        limit (float): 编码猜测比重
    """
    self._confidence = limit

  def hook_encoding(self) -> None:
    # gb2312 部分编码不识别,gbk完全兼容,因此替换 gb2312 为 gbk
    if self.from_encoding and self.from_encoding.lower() == 'gb2312':
      self.from_encoding = 'gbk'

    if self.to_encoding and self.to_encoding.lower() == 'gb2312':
      self.to_encoding = 'gbk'

  def _read_file_action(self) -> bool:
    with self.input.open('rb') as f:
      self._content: bytes = f.read()
    return True

  def _write_file_action(self) -> bool:
    need_write = self._changed or (self.output != self.input and self.no_change_copy_file)

    if need_write:
      make_sure_file_path(self.output)
      with self.output.open('wb') as f:
        f.write(self._content)
      return True
    return False

  def _guess_input_output_encoding(self, result: FileConverterResult) -> bool:
    if self._guessed:
      return True
    if not self.from_encoding:
      attrs = get_binary_encoding(self._content)
      if attrs['confidence'] < self._confidence:
        result.failed().failed_reson(_('检测文件 {} 编码 {} 精确度太低: {}, 最小处理精确度: {}').format(
            self.input, attrs['encoding'], attrs['confidence'], self._confidence))
        return False
      self.from_encoding = attrs['encoding']

    # 规范化编码字符串,后续可以直接字符串比较编码
    info = codecs.lookup(self.from_encoding)
    if info:
      self.from_encoding = info.name
    else:
      result.failed().failed_reson(_('输入文件 {} 编码不支持: {}').format(self.input, self.from_encoding))
      return False

    if not self.to_encoding:
      self.to_encoding = self.from_encoding
    else:
      info = codecs.lookup(self.to_encoding)
      if info:
        self.to_encoding = info.name
      else:
        result.failed().failed_reson(_('输入文件 {} 不能转换为不支持的编码: {}').format(self.input, self.to_encoding))
        return False
    self.hook_encoding()
    self._guessed = True
    return True

  def _encoding_transform_action(self, result: FileConverterResult) -> bool:
    """编码转换之前需要猜测编码
    """
    # 第一步猜测输入编码
    if not self._guess_input_output_encoding(result):
      return False
    # 第三步转换内容的编码
    if self.from_encoding == self.to_encoding:
      result.unchanged()
      return True
    try:
      self._content: str = self._content.decode(self.from_encoding)
      self._content: bytes = self._content.encode(self.to_encoding)
      self.callback.transform_encoding(
          self.input, self.output, self.from_encoding, self.to_encoding)
      self._changed = True
      result.changed().add_info(_('转换文件 {} 编码成功: {} =====> {}').format(self.input, self.from_encoding, self.to_encoding))
    except UnicodeDecodeError as e:
      result.failed().failed_reson(_('文件 {} 编码 {} 与实际不匹配, 失败原因: {}').format(self.input, self.from_encoding, str(e)))
      return False
    except UnicodeEncodeError as e:
      result.failed().failed_reson(_('文件 {} 编码转换错误: {} =====> {}, 失败原因: {}').format(
          self.input, self.from_encoding, self.to_encoding, str(e)))
      return False
    return True

  def _replace_bytes_action(self, result: FileConverterResult) -> bool:
    from_bytes = self._from_replaces[self._repalce_index]
    to_bytes = self._to_replaces[self._repalce_index]
    self._repalce_index += 1
    if from_bytes == to_bytes:
      result.unchanged()
      return True
    old_content = self._content
    old_len = len(old_content)
    self._content = old_content.replace(from_bytes, to_bytes)
    changed = old_len != len(self._content) or old_content != self._content
    self._changed |= changed
    if changed:
      self.callback.replace_content(self.input, self.output, from_bytes, to_bytes)
      result.changed().add_info(_('替换文件 {} 内容成功: {} =====> {}').format(self.input, from_bytes, to_bytes))
    else:
      result.unchanged()
    return True

  def _chinese_transform_action(self, result: FileConverterResult) -> bool:
    if not self._guess_input_output_encoding(result):
      return False
    if self.from_encoding == self.to_encoding:
      result.unchanged()
      return True
    try:
      content = self._content.decode(self.from_encoding)
      if is_contains_chinese(content):
        self._content: bytes = content.encode(self.to_encoding)
        self._changed = True
        self.callback.transform_chinese(self.input, self.output, self.from_encoding, self.to_encoding)
        result.changed().add_info(_('转换包含中文的文件 {} 编码: {} =====> {}').format(self.input, self.from_encoding, self.to_encoding))
    except UnicodeDecodeError as e:
      result.failed().failed_reson('文件 {} 编码 {} 与实际不匹配, 失败原因: {}'.format(self.input, self.from_encoding, str(e)))
      return False
    except UnicodeEncodeError as e:
      result.failed().failed_reson(_('文件 {} 编码转换错误: {} =====> {}, 失败原因: {}').format(
          self.input, self.from_encoding, self.to_encoding, str(e)))
      return False
    return True

  def _check_encoding_action(self, result: FileConverterResult) -> bool:
    if not self._guess_input_output_encoding(result):
      return False
    attrs = get_binary_encoding(self._content)
    if attrs['confidence'] < self._confidence:
      result.failed().failed_reson(_('检测文件 {} 编码 {} 精确度太低: {}, 最小处理精确度: {}').format(
          self.input, attrs['encoding'], attrs['confidence'], self._confidence))
      return False
    encoding = attrs['encoding']
    encoding = codecs.lookup(encoding).name
    # ascii 编码则可以任意转换
    ret = self.from_encoding == encoding or encoding == 'ascii'
    if not ret:
      self.callback.check_encoding(self.input, self.output, encoding, self.from_encoding)
      result.failed().failed_reson(_('检测文件 {} 编码不匹配: {} =====> {}').format(self.input, encoding, self.from_encoding))
    return ret

  def add_action(self, action: FileConvertAction, **kwargs) -> None:
    if action == FileConvertAction.transform_encoding:
      self._actions.append(FileConverter._encoding_transform_action)
    elif action == FileConvertAction.chinese_transform_encoding:
      self._actions.append(FileConverter._chinese_transform_action)
    elif action == FileConvertAction.crlf_to_lf:
      self._from_replaces.append(b'\r\n')
      self._to_replaces.append(b'\n')
      self._actions.append(FileConverter._replace_bytes_action)
    elif action == FileConvertAction.lf_to_crlf:
      self._from_replaces.append(b'\n')
      self._to_replaces.append(b'\r\n')
      self._actions.append(FileConverter._replace_bytes_action)
    elif action == FileConvertAction.replace_content:
      from_bytes = kwargs.pop('from', None)
      to_bytes = kwargs.pop('to', None)
      if from_bytes == to_bytes:
        logging.warning(_('转换内容前后一致 {} =====> {}').format(from_bytes, to_bytes))
        return
      if from_bytes is None:
        from_bytes = b''
      if to_bytes is None:
        to_bytes = b''
      self._from_replaces.append(from_bytes)
      self._to_replaces.append(to_bytes)
      self._actions.append(FileConverter._replace_bytes_action)
    elif action == FileConvertAction.check_encoding:
      self._actions.append(FileConverter._check_encoding_action)

  def execute(self) -> FileConverterResult:
    """执行action动作集合
    动作执行过程如下:
      1. 读文件 action, 将文件内容以二进制格式读取
      2. 执行添加的 action, 动作执行前后都应该将内容恢复到 bytes 类型
      3. 写文件 action, 以二进制格式写入文件,在此动作之前发送的所有错误均不会污染文件,只有该动作异常时才可能导致文件损坏

    Returns:
        FileConverterResult: 文件转换结果
    """
    result = FileConverterResult()
    # 可能重复使用,因此重置编码猜测
    self._guessed = False
    self._changed = False
    self._repalce_index = 0
    self._get_output()
    try:
      self._read_file_action()
      for action in self._actions:
        if not action(self, result) or result.is_failed() or not self.callback.action_executed(self.input, self._get_output(), result):
          return result
      self._write_file_action()
    except Exception as e:
      # 正常操作下是不会抛出异常的,代码存在问题
      result.exception_occurs().failed_reson(_('操作发生异常: {}').format(e))
    return result
