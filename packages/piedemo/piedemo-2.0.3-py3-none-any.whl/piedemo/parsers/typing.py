import inspect


def parse(fn):
    input_types = inspect.getfullargspec(fn).annotations
    if 'return' in input_types:
        input_types.pop('return')
    return input_types, fn
