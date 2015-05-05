import pika

class RemoteChannel(object):
    def __init__(self, worker_cfg):
        self.credentials = pika.PlainCredentials(worker_cfg['username'],
                                                 worker_cfg['password'])
        self.parameters = pika.ConnectionParameters(worker_cfg['host'],
                                                    worker_cfg['port'],
                                                    worker_cfg['vhost'],
                                                    self.credentials)
        self.connection = pika.BlockingConnection(parameters=self.parameters)
        self.channel = self.connection.channel()
        self.exchange = worker_cfg['exchange']
        #self.routing_key = worker_cfg['routing_key']        