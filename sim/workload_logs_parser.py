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

        self.test_data = df.sample(n=size)
        self.train_data = df

    def get_jobs(self) -> list[Job]:
        jobs = []
        min_submit_time = self.test_data['submit time'].min()
        for index, row in self.test_data.iterrows():
            job = Job(int((row['submit time'] - min_submit_time)/10000), index, row['user id'], row['run time'], row['cpu used'], row['memory used'])
            jobs.append(job)

        return jobs

    def get_train_data(self):
        return self.train_data