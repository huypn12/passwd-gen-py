import pika
import json
from remote_channel import RemoteChannel



class MasterAgent(object):
    
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

        self.request_rkey = 'request'
        self.request_queue = self.channel.queue_declare(exclusive=True)
        self.request_queue_id = self.request_queue.method.queue
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.request_queue_id,
                                routing_key='REQUEST')

        self.report_rkey = 'report'
        self.report_queue = self.channel.queue_declare(exclusive=True)
        self.report_queue_id = self.report_queue.method.queue
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.report_queue_id,
                                routing_key='REPORT')

        #------------ Worker setup
        self.workers = []
        self.data_source = None

    def register_worker(self, worker_cfg):
        self.workers.append(RemoteChannel(worker_cfg))

    def register_data_source(self, data_source):
        self.data_source = data_source

    ###########################################################################
    def publish_data(self, mesg, exchange):
        for worker in self.workers:
            if (worker.exchange == exchange):
                worker.channel.basic_publish(exchange=worker.exchange,
                                             routing_key='DATA',
                                             body=mesg)

    def publish_stop_cmd(self):
        for worker in self.workers:
            worker.channel.basic_publish(exchange=worker.exchange,
                                         routing_key='STOP',
                                         body='')
                                         
    ###########################################################################                                        
    def callback_request(self, ch, method, properties, body):
         print " [x] REQUEST: %r:%r" % (method.routing_key, body,)
         mesg = json.loads(body)
         if (mesg['cmd']=='request_data'):
             print "    Received data request from %s"%(mesg['from'],)
             data = self.data_source.get_chunk()
             if data == None:
                 print 'No more data to send.'
                 return
             else:
                 print "    Sending %s-sized chunk"%(len(data))
                 self.publish_data(json.dumps(data), mesg['from'])
    
    def callback_report(self, ch, method, properties, body):
        print " [x] REPORT: %r:%r" % (method.routing_key, body,)
        mesg = json.loads(body)
        creds = mesg['body']
        print "     Found valid credentials: %s"%(creds,)
        dump_valid_file_name = "data/valid_" + creds['username']
        with open(dump_valid_file_name, 'w') as valid_out:
            json.dump(creds, valid_out)
        print "     Rejecting all data request..."
        self.channel.queue_unbind(exchange=self.exchange_name,
                                  queue=self.request_queue_id,
                                  routing_key='REQUEST')
        self.channel.queue_purge(queue=self.request_queue_id)
        print "     Force all workers to stop searching..."
        self.publish_stop_cmd()
        
    ###########################################################################   
    def run(self):
        self.channel.basic_consume(self.callback_request,
                                   queue=self.request_queue_id,
                                   consumer_tag='tag.master.consume.request',
                                   no_ack=True)                             
        self.channel.basic_consume(self.callback_report,
                                   queue=self.report_queue_id,
                                   consumer_tag='tag.master.consume.report',
                                   no_ack=True)                                   
        self.channel.start_consuming()


if __name__ == 'name':
    master_agent = MasterAgent()



