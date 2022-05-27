from job import Job
import numpy as np
import pandas as pd

FEATURES_NUMBER = 18

class WorkloadLogsParser:
    def __init__(self, filename):
        self.filename = filename

    def get_jobs(self, size) -> list[Job]:
        with open(self.filename, 'r+', encoding='utf-8') as f:
            data = f.read().splitlines(True)
            
        data = [ line.replace('\n', '').replace('\t', ' ').split() for line in data if not line.startswith(';')]
        data = [[float(value) for value in line] for line in data if len(line) == FEATURES_NUMBER]


        np_data = np.array(data, dtype=int)

        labels = ['submit time', 'wait time', 'run time', 'cpu used', 'memory used','user id']
        np_data = np.delete(np_data, [0, 4, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17], 1)
        df = pd.DataFrame(np_data, columns=labels)

        jobs_to_parse = df.iloc[:size, :]
        jobs = []
        for index, row in jobs_to_parse.iterrows():
            job = Job(row['submit time'], index, row['user id'], row['run time'], row['cpu used'], row['memory used'])
            jobs.append(job)

        return jobs