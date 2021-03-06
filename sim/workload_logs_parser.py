from job import Job
import numpy as np
import pandas as pd

FEATURES_NUMBER = 18

class WorkloadLogsParser:
    def __init__(self, filename, size):
        with open(filename, 'r+', encoding='utf-8') as f:
            data = f.read().splitlines(True)
            
        data = [ line.replace('\n', '').replace('\t', ' ').split() for line in data if not line.startswith(';')]
        data = [[float(value) for value in line] for line in data if len(line) == FEATURES_NUMBER]


        np_data = np.array(data, dtype=int)

        labels = ['submit time', 'wait time', 'run time', 'cpu used', 'memory used','user id']
        np_data = np.delete(np_data, [0, 4, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17], 1)
        df = pd.DataFrame(np_data, columns=labels)

        data = df[df['cpu used'] > 0]


        self.test_data = data.sample(n=size)
        self.train_data = data

    def get_jobs(self) -> list[Job]:
        jobs = []
        submit_time = 0
        for index, row in self.test_data.iterrows():
            job = Job(submit_time, index, row['user id'], row['run time'], row['cpu used'], row['memory used'])
            submit_time = submit_time + 10
            jobs.append(job)

        return jobs

    def get_train_data(self):
        return self.train_data