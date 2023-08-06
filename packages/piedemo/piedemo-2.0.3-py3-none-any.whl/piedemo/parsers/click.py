import click
from click import Command
from enum import Enum
import inspect
from typing import Optional


def is_click_decorated(fn):
    return isinstance(fn, Command)


def click2types(p):
    t = p.type
    if isinstance(t, click.Choice):
        choices = t.choices
        ClickEnum = Enum._create_('Click' + p.name + 'Enum', {k: k for k in choices})
        ClickEnum.__piedemo_use_values = True
        output_type = ClickEnum
    elif isinstance(t, click.types.FuncParamType):
        output_type = inspect.getfullargspec(t.func).annotations['return']
    else:
        output_type = {
            click.INT: int,
            click.FLOAT: float,
            click.STRING: str,
        }[t]
    if not p.required and p.default is None:
        output_type = Optional[output_type]
    return output_type


def parse(fn: Command):
    input_types = {p.name: click2types(p) for p in fn.params}
    print(input_types)
    print(fn.callback)
    return input_types, fn.callback
