from job import Job
from manager import Manager
from node import Node

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
                print(f'job submit time: {job.get_submit_time()}')
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
            
            print(f'nodes working: {nodes_working}')
            print(f'current job: {self.current_job}')
            if not nodes_working and len(self.jobs) <= self.current_job:
                for job in self.jobs:
                    print(job.get_stats())
                return
            
            self.current_time += 1
            print(f'Current time: {self.current_time}')
