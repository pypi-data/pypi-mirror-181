# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import platform
import sys
from pathlib import Path

import colorama as ca

ca.init()
global_config_path = Path.home().joinpath('.devtools.ini')


class StdoutColorStreamHandler(logging.StreamHandler):
  def __init__(self, color=False):
    self.color = color
    super().__init__(sys.stdout)

  def format(self, record: logging.LogRecord) -> str:
    msg = super().format(record)
    if self.color:
      if record.levelno == logging.DEBUG:
        pass
      elif record.levelno == logging.INFO:
        msg = ca.Fore.GREEN + msg + ca.Style.RESET_ALL
      elif record.levelno == logging.WARNING:
        msg = ca.Fore.YELLOW + msg + ca.Style.RESET_ALL
    return msg

  def handle(self, record: logging.LogRecord) -> bool:
    if record.levelno >= logging.ERROR:
      return True
    return super().handle(record)


class StderrColorStreamHandler(logging.StreamHandler):
  """输出到 stderr 流,仅 error 及以上级别,fatal级别会退出程序
  """

  def __init__(self, color=False):
    self.color = color
    super().__init__(sys.stderr)
    self.level = logging.ERROR

  def format(self, record: logging.LogRecord) -> str:
    msg = super().format(record)
    if self.color:
      msg = ca.Fore.RED + msg + ca.Style.RESET_ALL
    return msg

  def handle(self, record: logging.LogRecord) -> bool:
    ret = super().handle(record)
    if record.levelno == logging.FATAL:
      sys.exit(-1)
    return ret


def init_color(out_color: bool | None = None, err_color: bool | None = None, **kwargs):
  """设置 logging 带颜色输出到控制台, ERROR 以上的级别输出到 stderr
  必须优先初始化,否则handler不生效

  filename  Specifies that a FileHandler be created, using the specified
            filename, rather than a StreamHandler.
  filemode  Specifies the mode to open the file, if filename is specified
            (if filemode is unspecified, it defaults to 'a').
  format    Use the specified format string for the handler.
  datefmt   Use the specified date/time format.
  style     If a format string is specified, use this to specify the
            type of format string (possible values '%', '{', '$', for
            %-formatting, :meth:`str.format` and :class:`string.Template`
            - defaults to '%').
  level     Set the root logger level to the specified level.
  stream    Use the specified stream to initialize the StreamHandler. Note
            that this argument is incompatible with 'filename' - if both
            are present, 'stream' is ignored.
  handlers  If specified, this should be an iterable of already created
            handlers, which will be added to the root handler. Any handler
            in the list which does not have a formatter assigned will be
            assigned the formatter created in this function.
  force     If this keyword  is specified as true, any existing handlers
            attached to the root logger are removed and closed, before
            carrying out the configuration as specified by the other
            arguments.
  encoding  If specified together with a filename, this encoding is passed to
            the created FileHandler, causing it to be used when the file is
            opened.
  errors    If specified together with a filename, this value is passed to the
            created FileHandler, causing it to be used when the file is
            opened in text mode. If not specified, the default value is
            `backslashreplace`.

  """

  handlers = kwargs.pop('handlers', [])
  if out_color is None:
    out_color = sys.stdout.isatty()
  if err_color is None:
    err_color = sys.stderr.isatty()
  n = len(logging.root.handlers)

  handlers.insert(0, StderrColorStreamHandler(err_color))
  handlers.insert(0, StdoutColorStreamHandler(out_color))
  force = kwargs.pop('force', True)
  logging.basicConfig(handlers=handlers, force=force, **kwargs)


def get_logger_file(path: str, level: int = logging.DEBUG, console_out: bool = True):
  """获取文件logger,如果路径为空则是默认的控制台logger

  Args:
      path (str): 文件路径
      level (int, optional): 指定log等级. 默认: logging.DEBUG.
      console_out (bool, optional): 是否输出到out控制台. 默认: True.

  Returns:
      object: logger 模块对象
  """
  log = logging.getLogger(path if path else 'file')
  file = Path(path)
  log.setLevel(level)
  if console_out:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    log.addHandler(console_handler)
  if file.is_file():
    file_handler = logging.FileHandler(path, 'a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    log.addHandler(file_handler)
  log.propagate = 0
  return log


def simple_logging_level():
  logging.addLevelName(logging.DEBUG, 'D')
  logging.addLevelName(logging.INFO, 'I')
  logging.addLevelName(logging.WARNING, 'W')
  logging.addLevelName(logging.ERROR, 'E')
  logging.addLevelName(logging.FATAL, 'F')


def is_windows():
  return platform.system() == 'Windows'


def is_linux():
  return platform.system() == 'Linux'


def is_macosx():
  return platform.system() == 'Darwin'


def init_simple_logger(log: logging.Logger):
  log.setLevel(logging.DEBUG)
  console_handler = StdoutColorStreamHandler(sys.stdout.isatty())
  err_handler = StderrColorStreamHandler(sys.stderr.isatty())
  console_handler.setFormatter(logging.Formatter('%(message)s'))
  err_handler.setFormatter(logging.Formatter('%(message)s'))
  log.handlers.clear()
  log.addHandler(console_handler)
  log.addHandler(err_handler)
  log.parent = None


simple_log = logging.getLogger('simple')
init_simple_logger(simple_log)
