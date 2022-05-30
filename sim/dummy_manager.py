from manager import Manager
from node import Node
from job import Job


class DummyManager(Manager):
    def __init__(self, train_dataset, nodes: list[Node]):
        self.nodes = nodes
        self.current_node = 0
        self.user_nodes = {}

    def find_node(self, job: Job) -> Node:
        if job.user_id in self.user_nodes:
            return self.nodes[self.user_nodes[job.user_id]]
        self.current_node = (self.current_node + 1) % len(self.nodes)
        self.user_nodes[job.user_id] = self.current_node
        return self.nodes[self.current_node]