from node import Node
from pretrained_manager import PretrainedManager
from workload_logs_parser import WorkloadLogsParser
from dummy_manager import DummyManager
from simulator import Simulator

if __name__ == '__main__':
    parser = WorkloadLogsParser('../test2.txt', 1000)

    # nodes
    node1 = Node(100, 50)
    node2 = Node(1000, 1500)
    nodes = [node1, node2]

    # manager
    manager = DummyManager([], nodes)
    pretrainedManager = PretrainedManager(parser.get_train_data(), nodes)

    # simulator
    simulator1 = Simulator(parser.get_jobs(), nodes, manager)
    simulator2 = Simulator(parser.get_jobs(), nodes, pretrainedManager)

    simulator1.simulate("dummy_times.png")
    simulator2.simulate("pretrained_times.png")
    
