import json

class Config(object):
    def __init__(self):
        self.master_config_file = 'config/master.cfg'
        self.worker_config_file = 'config/worker.cfg'
        self.master_conf = {}
        self.worker_conf = []
        
    def load_master_conf(self):
        with open(self.master_config_file) as f_master_conf:
            conf = json.load(f_master_conf)
            self.master_conf = conf
            
    def load_worker_conf(self):
        with open(self.worker_config_file) as f_worker_conf:
            conf = json.load(f_worker_conf)
            self.worker_conf = conf
            
    def load(self):
        self.load_master_conf()
        self.load_worker_conf()

if __name__ == '__main__':
    config = Config()
    config.load()
    print config.master_conf
    print config.worker_conf
    
        
        