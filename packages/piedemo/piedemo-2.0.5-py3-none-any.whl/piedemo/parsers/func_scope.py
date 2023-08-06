#!/usr/bin/env python
# coding=utf-8

import ast
import inspect
import types
import io
import re
from tokenize import tokenize, TokenError, COMMENT
from copy import copy


def get_function_body(func):
    func_code_lines, start_idx = inspect.getsourcelines(func)
    func_code = "".join(func_code_lines)
    arg = "(?:[a-zA-Z_][a-zA-Z0-9_]*)"
    arguments = r"{0}(?:\s*[,:= \.]*\s*{0})*".format(arg)
    func_def = re.compile(
        r"^[ \t]*def[ \t]*{}[ \t]*\(\s*({})?\s*\)[ \t]*:[ \t]*\n".format(
            func.__name__, arguments
        ),
        flags=re.MULTILINE,
    )
    defs = list(re.finditer(func_def, func_code))
    assert defs
    line_offset = start_idx + func_code[: defs[0].end()].count("\n") - 1
    func_body = func_code[defs[0].end():]
    return func_body, line_offset


def is_empty_or_comment(line):
    sline = line.strip()
    return sline == "" or sline.startswith("#")


def dedent_line(line, indent):
    for i, (line_sym, indent_sym) in enumerate(zip(line, indent)):
        if line_sym != indent_sym:
            start = i
            break
    else:
        start = len(indent)
    return line[start:]


def dedent_function_body(body):
    lines = body.split("\n")
    # find indentation by first line
    indent = ""
    for line in lines:
        if is_empty_or_comment(line):
            continue
        else:
            indent = re.match(r"^\s*", line).group()
            break

    out_lines = [dedent_line(line, indent) for line in lines]
    return "\n".join(out_lines)


class func2locals(object):
    def __init__(self, func):
        self.func = func
        self.global_vars = self.func.__globals__
        filename = inspect.getfile(func)
        body, line_offset = get_function_body(func)
        body_source = dedent_function_body(body)
        body_code = compile(body_source, filename, "exec", ast.PyCF_ONLY_AST)
        body_code = ast.increment_lineno(body_code, n=line_offset)
        body_code = compile(body_code, filename, "exec")
        self.body_code = body_code

    def __call__(self, **kwargs):
        old_locals = locals()
        old_locals.update(kwargs)
        new_locals = copy(old_locals)
        eval(self.body_code, copy(self.global_vars), new_locals)
        output_keys = set(new_locals.keys()).difference(old_locals.keys()).union(kwargs.keys())
        return {key: new_locals[key] for key in output_keys}
