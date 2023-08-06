import os
from .base import Field
import math
from itertools import tee


class VStack(Field):
    def __init__(self, fields,
                 xs=""):
        super(VStack, self).__init__(None)
        self.fields = fields
        if not isinstance(xs, list):
            xs = [xs for _ in range(len(self.fields))]
        self.xs = xs

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.fields[index]
        elif isinstance(index, str):
            return {f.name: f for f in self.fields if hasattr(f, 'name')}[index]
        else:
            raise IndexError

    def generate(self):
        return [[{"content": f.generate(), "xs": self.xs[i]}] for i, f in enumerate(self.fields)]

    def children(self):
        return sum([f.children() for f in self.fields], [])

    def clear(self):
        for f in self.fields:
            f.clear()

    def __repr__(self):
        return "VStack([%s])" % ',\n'.join([repr(f) for f in self.fields])


class HStack(Field):
    def __init__(self, fields,
                 xs=""):
        super(HStack, self).__init__(None)
        self.fields = fields
        if not isinstance(xs, list):
            xs = [xs for _ in range(len(self.fields))]
        self.xs = xs

    def __getitem__(self, index: int):
        if isinstance(index, int):
            return self.fields[index]
        elif isinstance(index, str):
            return {f.name: f for f in self.fields if hasattr(f, 'name')}[index]
        else:
            raise IndexError

    def generate(self):
        return [[{"content": f.generate(), "xs": self.xs[i]} for i, f in enumerate(self.fields)]]

    def children(self):
        return sum([f.children() for f in self.fields], [])

    def clear(self):
        for f in self.fields:
            f.clear()

    def __repr__(self):
        return "HStack([%s])" % ',\n'.join([repr(f) for f in self.fields])


class Stack(Field):
    def __init__(self, fields,
                 xs="4"):
        super(Stack, self).__init__(None)
        self.fields = fields
        if not isinstance(xs, list):
            xs = [xs for _ in range(len(self.fields))]
        self.xs = xs

    def __getitem__(self, index: int):
        if isinstance(index, int):
            return self.fields[index]
        elif isinstance(index, str):
            return {f.name: f for f in self.fields if hasattr(f, 'name')}[index]
        else:
            raise IndexError

    def generate(self):
        rows = []
        for i in range(int(math.ceil(len(self.fields) / 3))):
            cols = []
            for j in range(3 * i, min(3 * i + 3, len(self.fields))):
                cols.append({"content": self.fields[j].generate(), "xs": self.xs[j]})
            rows.append(cols)
        return rows

    def children(self):
        return sum([f.children() for f in self.fields], [])

    def clear(self):
        for f in self.fields:
            f.clear()

    def __repr__(self):
        return "Stack([%s])" % ',\n'.join([repr(f) for f in self.fields])


def stack_contents(contents):
    return [[{"content": content, "xs": ""}
             for content in contents]]
