from node import Node
from kmeans_manager import KmeansManager
from workload_logs_parser import WorkloadLogsParser
from dummy_manager import DummyManager
from simulator import Simulator

if __name__ == '__main__':
    parser = WorkloadLogsParser('../test2.txt')

    # nodes
    node1 = Node(1, 100, 100)
    node2 = Node(2, 200, 200)
    node3 = Node(5, 10, 10)
    node4 = Node(10, 10, 10)
    nodes = [node1, node2, node3, node4]

    # jobs
    jobs = parser.get_jobs(100)

    # manager
    # manager = DummyManager([], nodes)
    manager = KmeansManager(parser.get_train_data(), nodes)

    # simulator
    simulator = Simulator(jobs, nodes, manager)

    simulator.simulate()
    
