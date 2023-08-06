import io
import base64
from .base import OutputField
import pandas as pd
from typing import Optional


class OutputTableField(OutputField):
    def __init__(self, name):
        super(OutputTableField, self).__init__(name=name)
        self.table: Optional[pd.DataFrame] = None

    def set_output(self, data: pd.DataFrame):
        self.table = data

    def generate(self):
        columns = self.table.columns
        if not isinstance(columns, pd.MultiIndex):
            columns = [columns.tolist()]
        else:
            # columns = [columns.get_level_values(i).tolist() for i in range(len(columns.levels))]
            levels = [[] for _ in range(self.table.columns.nlevels)]
            for col in self.table.columns:
                for i in range(len(levels)):
                    if col[i] not in levels[i]:
                        levels[i].append(col[i])

            columns = levels

        return {
            "card": "OutputTableCard",
            "data": {
                "name": self.name,
                "headers": columns,
                "rows": [[str(self.table[c][i]) for c in self.table.columns] for i in range(len(self.table))]
            }
        }

    def clear(self):
        self.table = None

    def __repr__(self):
        return "OutputTableField(%s)" % self.name
