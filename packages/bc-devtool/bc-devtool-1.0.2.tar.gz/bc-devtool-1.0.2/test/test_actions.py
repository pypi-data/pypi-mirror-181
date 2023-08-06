# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import logging
from ctypes import ArgumentError

import pytest
from bc_devtool import arg_actions as aa

logging.basicConfig(level=logging.INFO)


class ActionsTest:
  def __init__(self, parser: argparse.ArgumentParser, input: argparse.Action, output: argparse.Action) -> None:
    self.parser = parser
    self.input = input
    self.output = output


@pytest.fixture
def create_action_param():
  parser = argparse.ArgumentParser('test')
  input = parser.add_argument('-i', '--input', help='input argument')
  output = parser.add_argument('-o', '--output', help='output argument')
  return ActionsTest(parser, input, output)


def test_true_required_action(create_action_param: ActionsTest):
  parser = create_action_param.parser
  parser.add_argument('-q', action=aa.TrueRequiredAction, action_type='store_true',
                      actions=[create_action_param.input, create_action_param.output], help='test request 1')

  try:
    parser.parse_args(args=['-q', '123', '-i', 'input'])
    assert False
  except SystemExit as e:
    assert e.code == 2


def test_false_required_action(create_action_param: ActionsTest):
  parser = create_action_param.parser
  parser.add_argument('-q', action=aa.FalseRequiredAction, action_type='store_true',
                      actions=[create_action_param.input, create_action_param.output], help='test request 1')

  try:
    parser.parse_args(args=['-q', '123', '-i', 'input'])
    assert False
  except SystemExit as e:
    assert e.code == 2


def test_required_action_value(create_action_param: ActionsTest):
  parser = create_action_param.parser
  parser.add_argument('-q', '--req', action=aa.TrueRequiredAction, action_type='store_true',
                      actions=[create_action_param.input, create_action_param.output], help='test request 1')

  args = parser.parse_args(args=['-q', '-i', 'input', '-o', 'output'])
  assert args.req == True
  assert args.input == 'input'
  assert args.output == 'output'


def test_required_action_value2(create_action_param: ActionsTest):
  parser = create_action_param.parser
  parser.add_argument('-q', '--req', action=aa.TrueRequiredAction, action_type='store_false',
                      actions=[create_action_param.input, create_action_param.output], help='test request 1')

  args = parser.parse_args(args=['-q', '-i', 'input', '-o', 'output'])
  assert args.req == False
  assert args.input == 'input'
  assert args.output == 'output'


def test_required_action_argument_error(create_action_param: ActionsTest):
  parser = create_action_param.parser
  try:
    parser.add_argument('-q', '--req', action=aa.TrueRequiredAction, action_type='str',
                        actions=[create_action_param.input, create_action_param.output], help='test request 1')
    args = parser.parse_args(args=['-q', '-i', 'input', '-o', 'output'])
    assert False
  except ArgumentError as e:
    assert True


def test_required_action_value_str(create_action_param: ActionsTest):
  parser = create_action_param.parser
  parser.add_argument('-q', '--req', action=aa.TrueRequiredAction,
                      actions=[create_action_param.input, create_action_param.output], help='test request 1')

  args = parser.parse_args(args=['-q', '123', '-i', 'input', '-o', 'output'])
  assert args.req == '123'
  assert args.input == 'input'
  assert args.output == 'output'


def test_special_str_required_action(create_action_param: ActionsTest):
  parser = create_action_param.parser
  required: aa.TrueRequiredAction = parser.add_argument(
      '-q', '--req', action=aa.TrueRequiredAction, bind_value=True, help='test request 1')
  required.add_required('123', create_action_param.input)
  try:
    args = parser.parse_args(args=['-q', '123', '-o', 'output'])
  except SystemExit as e:
    assert e.code == 2


def test_special_str_required_action2(create_action_param: ActionsTest):
  parser = create_action_param.parser
  required: aa.FalseRequiredAction = parser.add_argument(
      '-q', '--req', action=aa.FalseRequiredAction, bind_value=True, help='test request 1')
  required.add_required('123', create_action_param.input)
  args = parser.parse_args(args=['-q', '123', '-o', 'output'])
  assert args.req == '123'
  assert args.output == 'output'
  assert args.input == None
