import os
import pickle
from pathlib import Path


def try_int(x, other=None):
    try:
        return int(x)
    except:
        return other


class IntStorage(int):
    pass


class StrStorage(str):
    pass


class FloatStorage(float):
    pass


class FrozenSetStorage(frozenset):
    pass


class DictStorage(dict):
    pass


def make_storage(v):
    mapping = {
        int: IntStorage,
        float: FloatStorage,
        str: StrStorage,
        frozenset: FrozenSetStorage,
        dict: DictStorage,
    }
    if v.__class__ in mapping:
        return mapping[v.__class__](v)
    return v


class Cache(object):
    def __init__(self, path: Path):
        path = Path(path)
        path.mkdir(exist_ok=True)
        self.path = path

    def new_id(self):
        stored = set([try_int(p.name[:-4])
                      for p in self.path.iterdir()
                      if p.name.endswith('.pkl')])
        if -1 in stored:
            stored.remove(None)
        return max(stored, default=-1) + 1

    def get(self, data_id):
        data_path = self.path / f"{data_id}.pkl"
        with data_path.open('rb') as f:
            return pickle.load(f)

    def store(self, **data):
        data_id = self.new_id()
        data_path = self.path / f"{data_id}.pkl"
        with data_path.open('wb') as f:
            pickle.dump(data, f)
        return data_id
