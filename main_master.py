from data_source import DataSource
from master_agent import MasterAgent
from config import Config

print "------ Distributed Email Password Bruteforce -----\n"
print "Starting master node ..."
config = Config()
config.load()

master_conf = config.master_conf
print "Master node running parameter: ", master_conf
master_node = MasterAgent(master_conf)
print "Master node created successfully: ", master_node

worker_conf = config.worker_conf
for w_cfg in worker_conf:
    master_node.register_worker(w_cfg)

acc_name = "lan_ho"
data_source = DataSource(acc_name)
master_node.register_data_source(data_source)

master_node.run()

