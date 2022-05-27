from manager import Manager
from node import Node
from job import Job


class DummyManager(Manager):
    def __init__(self, train_dataset, nodes: list[Node]):
        self.nodes = nodes
        self.current_node = 0

    def find_node(self, job: Job) -> Node:
        self.current_node = (self.current_node + 1) % len(self.nodes)
        return self.nodes[self.current_node]