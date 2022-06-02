from manager import Manager
from node import Node
from job import Job
from sklearn import preprocessing
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture




class PretrainedManager(Manager):
    def __init__(self, train_dataset, nodes: list[Node]):
        self.nodes = nodes
        self.current_index = 0
        self.user_nodes = {}
        train_data = train_dataset[train_dataset['cpu used'] > 0].copy()
        train_data['count'] = train_data.groupby('user id')['user id'].transform('count')
        grouped = train_data.groupby('user id').mean()
        grouped.pop('wait time')
        grouped.pop('submit time')
        grouped.pop('run time')
        user_profiles = grouped.to_numpy()
        scaler = preprocessing.StandardScaler().fit(user_profiles)
        user_profiles = scaler.transform(user_profiles)
        mixture = GaussianMixture(n_components=3).fit(user_profiles)
        predict = mixture.predict(user_profiles)
        cluster0 = grouped[ predict == 0]
        cluster1 = grouped[ predict == 1]
        cluster2 = grouped[ predict == 2]
        clusters = [cluster0, cluster1, cluster2]
        # find clusters with the most complex jobs
        max_cpu = 0
        max_index = 0
        for index, cluster in enumerate(clusters):
            if cluster.shape[0] > 100:
                cpu = cluster['cpu used'].mean()
                if cpu > max_cpu:
                    max_cpu = cpu
                    max_index = index
        
        # assingn those users to the best node
        for index, _ in clusters[max_index].iterrows():
            self.user_nodes[index] = 1
        
        # find clusters with the most frequent jobs
        max_count = 0
        max_count_index = 0
        for index, cluster in enumerate(clusters):
            if cluster.shape[0] > 100:
                count = cluster['count'].mean()
                if count > max_count:
                    max_count = count
                    max_count_index = index

        # assingn those users to the nearest node
        if max_index != max_count_index:
            for index, _ in clusters[max_count_index].iterrows():
                self.user_nodes[index] = 0


    def find_node(self, job: Job) -> Node:
        available_nodes = [0, 1]
        if job.user_id in self.user_nodes:
            return self.nodes[self.user_nodes[job.user_id]]
        self.current_index = (self.current_index + 1) % len(available_nodes)
        self.user_nodes[job.user_id] = available_nodes[self.current_index]
        return self.nodes[available_nodes[self.current_index]]