from node import Node
from pretrained_manager import PretrainedManager
from workload_logs_parser import WorkloadLogsParser
from dummy_manager import DummyManager
from simulator import Simulator
import matplotlib.pyplot as plt


if __name__ == '__main__':
    parser = WorkloadLogsParser('../test2.txt', 1000)

    # nodes
    node1 = Node(100, 0)
    node2 = Node(10000, 90)
    nodes = [node1, node2]

    # manager
    manager = DummyManager([], nodes)
    pretrainedManager = PretrainedManager(parser.get_train_data(), nodes)

    # simulator
    simulator1 = Simulator(parser.get_jobs(), nodes, manager)
    simulator2 = Simulator(parser.get_jobs(), nodes, pretrainedManager)

    dummy_means = simulator1.simulate()
    pretrained_means = simulator2.simulate()

    print(dummy_means)
    print(pretrained_means)

    wait_times = [dummy_means[0], pretrained_means[0]]
    plt.figure(figsize=(16, 12))
    plt.title = 'Wait times'
    plt.ylabel('Time [s]')
    plt.bar(['Dummy manager', 'Pretrained manager'], wait_times)
    plt.savefig(f'outputs/wait_times.png')
    plt.close()
    run_times = [dummy_means[1], pretrained_means[1]]
    plt.figure(figsize=(16, 12))
    plt.title = 'Run times'
    plt.ylabel('Time [s]')
    plt.bar(['Dummy manager', 'Pretrained manager'], run_times)
    plt.savefig(f'outputs/run_times.png')
    plt.close()

