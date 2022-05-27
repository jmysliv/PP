from node import Node
from workload_logs_parser import WorkloadLogsParser
from dummy_manager import DummyManager
from simulator import Simulator

if __name__ == '__main__':
    parser = WorkloadLogsParser('../test2.txt')

    # nodes
    node1 = Node(100, 100, 100)
    node2 = Node(200, 200, 200)
    nodes = [node1, node2]

    # jobs
    jobs = parser.get_jobs(100)

    # manager
    manager = DummyManager([], nodes)

    # simulator
    simulator = Simulator(jobs, nodes, manager)

    simulator.simulate()
    
