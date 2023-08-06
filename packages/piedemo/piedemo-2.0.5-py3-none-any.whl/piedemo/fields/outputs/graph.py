import networkx as nx
from pyvis.network import Network
import io
from .base import OutputField


class OutputGraphField(OutputField):
    def __init__(self, name, g: Network = None):
        super(OutputGraphField, self).__init__(name=name)
        self.g = g

    def set_output(self, g: Network):
        self.g = g

    def generate(self):
        nodes, edges, heading, height, width, options = self.g.get_network_data()
        return {
            "card": "OutputGraphCard",
            "data": {
                "name": self.name,
                "graph": {
                    "nodes": nodes,
                    "edges": edges
                },
                "options": options
            }
        }

    def clear(self):
        self.g = None
