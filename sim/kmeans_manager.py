from manager import Manager
from node import Node
from job import Job
from sklearn import preprocessing
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans




class KmeansManager(Manager):
    def __init__(self, train_dataset, nodes: list[Node]):
        self.nodes = nodes
        self.current_node = 0
        self.user_nodes = {}
        train_dataset['count'] = train_dataset.groupby('user id')['user id'].transform('count')
        grouped = train_dataset.groupby('user id').mean()
        grouped.pop('wait time')
        grouped.pop('submit time')
        user_profiles = grouped.to_numpy()
        scaler = preprocessing.StandardScaler().fit(user_profiles)
        user_profiles = scaler.transform(user_profiles)
        kmeans = KMeans(n_clusters=4).fit(user_profiles)
        labels = kmeans.labels_
        cluster0 = grouped[ labels == 0]
        cluster1 = grouped[ labels == 1]
        cluster2 = grouped[ labels == 2]
        cluster3 = grouped[ labels == 3]
        clusters = [cluster0, cluster1, cluster2, cluster3]
        # find clusters with the most complex jobs
        max_runtime = 0
        max_index = 0
        for index, cluster in enumerate(clusters):
            runtime = cluster['run time'].mean()
            if runtime > max_runtime:
                max_runtime = runtime
                max_index = index
        
        # assingn those users to the best node
        for index, _ in clusters[max_index].iterrows():
            self.user_nodes[index] = 3


    def find_node(self, job: Job) -> Node:
        if job.user_id in self.user_nodes:
            return self.nodes[self.user_nodes[job.user_id]]
        self.current_node = (self.current_node + 1) % len(self.nodes)
        self.user_nodes[job.user_id] = self.current_node
        return self.nodes[self.current_node]