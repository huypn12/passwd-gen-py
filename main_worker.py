from worker_agent import WorkerAgent
from config import Config  

print "------ Distributed Email Password Bruteforce -----\n"
print "Starting WorkerNode..."

config = Config()
config.load()

master_conf = config.master_conf
worker_conf = config.worker_conf
workers = []
for w_conf in worker_conf:
    worker_node = WorkerAgent(w_conf)
    worker_node.register_master(master_conf)
    workers.append(worker_node)
for w in workers:
    w.run()
