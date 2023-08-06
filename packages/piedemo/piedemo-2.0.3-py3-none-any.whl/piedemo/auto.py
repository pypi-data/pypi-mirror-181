import os
import inspect
from PIL import Image
import numpy as np
import pandas as pd
import json
from enum import Enum, EnumMeta
import importlib
from .parsers.click import is_click_decorated, parse as parse_click
from .parsers.typing import parse as parse_typing
from .parsers.func_scope import func2locals
from .fields.inputs.image import InputImageField
from .fields.inputs.ranged_int import InputRangedIntField
from .fields.inputs.text import InputTextField
from .fields.inputs.int_list import InputIntListField
from .fields.inputs.ranged_float import InputRangedFloatField
from .fields.inputs.tuple import InputTupleField
from .fields.inputs.choice import InputChoiceField
from .fields.inputs.bool import InputBoolField
from .fields.outputs.base import OutputField
from .fields.outputs.image import OutputImageField
from .fields.grid import VStack, HStack, Stack
from .fields.outputs.table import OutputTableField
from .fields.outputs.json import OutputJSONField
from .fields.outputs.piegraph import PieGraph, OutputPieGraphField
from typing_extensions import Annotated
from typing import List, Union, Tuple, Optional


def IntRange(minValue,
             maxValue,
             stepValue=1,
             label=""):
    return json.dumps({
        "minValue": minValue,
        "maxValue": maxValue,
        "stepValue": stepValue,
        "formatLabel": label
    })


def input_types2fields(t, **kwargs):
    if hasattr(t, "__origin__"):
        if t.__origin__ == Union and t.__args__[1] is type(None):
            kwargs.update({'optional': True})
            t = t.__args__[0]
            return input_types2fields(t, **kwargs)

        if t.__origin__ == tuple:
            n = len(t.__args__)
            if set(t.__args__).union({int, str, float}) != {int, str, float}:
                raise NotImplementedError("Support only int, str, float")
            kwargs.update({'types': t.__args__})
            t = Tuple

    if isinstance(t, Annotated[str, 1].__class__):
        kwargs.update(json.loads(t.__metadata__[0]))
        t = t.__args__[0]

    if isinstance(t, EnumMeta):
        choices = [c.name for c in list(t._member_map_.values())]
        kwargs.update({'choices': choices})
        kwargs.update({'enum_type': t})
        if hasattr(t, '__piedemo_use_values') and t.__piedemo_use_values:
            kwargs.update({"use_values": True})

        t = Enum

    if t == bool:
        flags = [kwargs.get('name')]
        kwargs.update({"flags": flags})

    return {
        Image.Image: InputImageField,
        int: InputRangedIntField,
        List[int]: InputIntListField,
        str: InputTextField,
        float: InputRangedFloatField,
        Tuple: InputTupleField,
        Enum: InputChoiceField,
        bool: InputBoolField,
    }[t](**kwargs)


def output_types2fields(t, **kwargs):
    return {
        Image.Image: OutputImageField,
        pd.DataFrame: OutputTableField,
        dict: OutputJSONField,
        list: OutputJSONField,
        int: OutputJSONField,
        float: OutputJSONField,
        type(None): OutputJSONField,
        str: OutputJSONField,
        bool: OutputJSONField,
        PieGraph: OutputPieGraphField
    }[t](**kwargs)


def get_dummy_input(t):
    if t == List[int]:
        return [1]

    if t == Image.Image:
        return Image.new('RGB', size=(10, 10))

    if isinstance(t, EnumMeta):
        return list(t._member_map_.values())[0]

    if hasattr(t, "__origin__"):
        if t.__origin__ == tuple:
            n = len(t.__args__)
            if set(t.__args__).union({int, str, float}) != {int, str, float}:
                raise NotImplementedError("Support only int, str, float")
            return tuple([t.__args__[i]() for i in range(n)])

        if t.__origin__ == Union and t.__args__[1] is t.__args__[1] is type(None):
            t = t.__args__[0]
            return get_dummy_input(t)

    return t()


def autotyping(dummy_input):
    return {key: type(value) for key, value in dummy_input.items()}


def introspect(fn,
               inrow=False,
               incol=False):
    if inrow:
        Stack_ = HStack
    elif incol:
        Stack_ = VStack
    else:
        Stack_ = Stack

    if is_click_decorated(fn):
        input_types, fn = parse_click(fn)
    else:
        input_types, fn = parse_typing(fn)
    dummy_input = {k: get_dummy_input(v) for k, v in input_types.items()}
    dummy_output = fn(**dummy_input)
    if dummy_output is None:
        fn = func2locals(fn)
        dummy_output = fn(**dummy_input)

    output_types = autotyping(dummy_output)

    input_field = Stack_([input_types2fields(t, name=k) for k, t in input_types.items()])
    output_field = Stack_([output_types2fields(t, name=k) for k, t in output_types.items()])
    print("Inputs:")
    print(input_field)
    print("Outputs: ")
    print(output_field)
    return {
        "inputs": input_field,
        "outputs": output_field,
        "demo_function": fn
    }


def import_function(path):
    module, fn_name = path.split(':')
    module = importlib.import_module(module)
    fn = getattr(module, fn_name)
    return fn, fn_name
