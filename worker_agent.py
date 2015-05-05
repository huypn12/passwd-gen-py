# auf Knoten Arbeiter eingesetzt werden

import pika
import json
from remote_channel import RemoteChannel
from email_auth import EmailAuth

class WorkerAgent(object):
    ###########################################################################
    def __init__(self, amqp_cfg):
        #----------- Master parameter
        self.credentials = pika.PlainCredentials(amqp_cfg['username'],
                                                 amqp_cfg['password'])
        self.parameters = pika.ConnectionParameters(amqp_cfg['host'],
                                                    amqp_cfg['port'],
                                                    amqp_cfg['vhost'],
                                                    self.credentials)
        self.connection = pika.BlockingConnection(parameters=self.parameters)
        self.channel = self.connection.channel()

        self.exchange_name = amqp_cfg['exchange']
        self.exchange = self.channel.exchange_declare(exchange=self.exchange_name,
                                                      type='direct')

        self.data_queue = self.channel.queue_declare(exclusive=True)
        self.data_queue_id = self.data_queue.method.queue#amqp_cfg['queue'] # Master node's request queue
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.data_queue_id,
                                routing_key='DATA')

        self.stop_queue = self.channel.queue_declare(exclusive=True)
        self.stop_queue_id = self.stop_queue.method.queue
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.stop_queue_id,
                                routing_key='STOP')
        #------------ Master connection
        self.master = None

    def register_master(self, master_cfg):
        self.master = RemoteChannel(master_cfg)


    ###########################################################################
    def request_data(self):
        request = {
            'from':self.exchange_name,
            'cmd':'request_data',
            'body':'something'
        }
        self.master.channel.basic_publish(exchange=self.master.exchange,
                                          routing_key='REQUEST',
                                          body=json.dumps(request))

    def report_valid(self, creds):
        report = {
            'from':self.exchange_name,
            'cmd':'report_valid',
            'body':json.dumps(creds)
        }
        self.master.channel.basic_publish(exchange=self.master.exchange,
                                          routing_key='REPORT',
                                          body=json.dumps(report))
    def process_response(self, mesg):
        loaded_mesg = json.loads(mesg)
        for creds in loaded_mesg:
            print "     Checking credentials: ", creds
            valid = EmailAuth.try_auth(creds)
            print "         ", valid
            if valid == True:
                self.report_valid(creds)
                return

    def process_stop_cmd(self):
        print "Received announcement from Master node: valid credentials is found."
        print "Cancel searching."
        self.channel.queue_purge(queue=self.data_queue_id)

    ###########################################################################

    def callback_data(self, ch, method, properties, body):
        #print " [x] %r:%r" % (method.routing_key, body,)
        self.process_response(body)
        self.request_data()

    def callback_stop(self, ch, method, properties, body):
        self.process_stop_cmd()

    def run(self):
        self.request_data()
        self.channel.basic_consume(self.callback_data,
                                   queue=self.data_queue_id,
                                   no_ack=True)
        self.channel.basic_consume(self.callback_stop,
                                   queue=self.stop_queue_id,
                                   no_ack=True)
        self.channel.start_consuming()


if __name__ == 'main':
    worker_agent = WorkerAgent()
