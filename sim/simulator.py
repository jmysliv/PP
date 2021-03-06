from job import Job
from manager import Manager
from node import Node
import numpy as np


class Simulator:
    def __init__(self, jobs: list[Job], nodes: list[Node], manager: Manager):
        self.jobs = jobs
        self.nodes = nodes
        self.manager = manager
        self.current_time = 0
        self.current_job = 0

    def simulate(self):
        while True:
            if len(self.jobs) > self.current_job:
                job = self.jobs[self.current_job]
                while job.get_submit_time() == self.current_time:
                    node = self.manager.find_node(job)
                    node.add_job(job, self.current_time)
                    self.current_job += 1
                    if len(self.jobs) == self.current_job:
                        break

                    job = self.jobs[self.current_job]

            nodes_working = False
            for node in self.nodes:
                if node.execute_jobs(self.current_time):
                    nodes_working = True
            
            if not nodes_working and len(self.jobs) <= self.current_job:
                stats = []
                for job in self.jobs:
                    stats.append(job.get_stats())
                np_stats = np.array(stats)
                means = np.mean(np_stats, axis=0)
                return means
            
            self.current_time += 1
