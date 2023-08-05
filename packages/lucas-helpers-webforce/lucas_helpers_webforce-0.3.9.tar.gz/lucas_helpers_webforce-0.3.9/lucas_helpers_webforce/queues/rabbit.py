import os, time, json
import threading

import pika
from pika.exceptions import AMQPConnectionError

service_name=os.environ["SERVICE_NAME"]
bus_events_exchange=os.environ["BUS_EVENTS_EXCHANGE"]
queue_name=f"service_{service_name}"

def callback(ch, method, properties, body):
    print(f"[{service_name}] Received %s" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


class Rabbit:
    def __init__(self) -> None:
        self.debug = True
        self.host = "message_broker"
        self.connection = None
        self.channel = None
        self.queue = None
    
    def __enter__(self):
        self.open_connection()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close_connection()
    
    def reset_values(self):
        self.connection = None
        self.channel = None
        self.queue = None
        print("values reseted")
    
    def log(self, *args):
        if(self.debug):
            print(args)
    
    def open_connection(self):
        if self.connection: 
            return self.connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        return self

    def get_connection(self):
        return self.connection
    
    def open_channel(self):
        if self.channel:
            return self.channel
        self.channel = self.connection.channel()
        return self

    def get_channel(self):
        return self.channel
    
    def set_exchange(self, **kwargs):
        self.open_connection()
        self.open_channel()
        self.channel.exchange_declare(**kwargs)
        return self
    
    def new_queue(self,**kwargs):
        self.queue = self.channel.queue_declare(**kwargs)
        return self
    
    def get_queue(self):
        return self.queue

    def bind_queue(self,**kwargs):
        self.channel.queue_bind(**kwargs)
        return self

    def connect_to_bus_events(self, events_handler=None):
        try:
            type_of_exchange='fanout'
            self.set_exchange(exchange=bus_events_exchange,exchange_type=type_of_exchange)
            self.new_queue(queue=queue_name,durable=True)
            self.bind_queue(exchange=bus_events_exchange,queue=queue_name,routing_key='')
            self.connection.close()
            print(f"{service_name} connected to Bus Events 🚌")
            self.reset_values()
            self.start_consuming_from_bus_events(events_handler)
        except AMQPConnectionError:
            print("AMQPConnectionError Waiting for RabbitMQ server to be online...")
            time.sleep(3)
            self.connect_to_bus_events()
        except Exception as e:
            print (e)
            print("ErrorConnectingToBusEvents")

    def start_consuming_from_bus_events(self,events_handler=None):
        self.open_connection()
        self.open_channel()
        print(f"[{service_name}] Waiting for messages.")
        self.channel.basic_qos(prefetch_count=1)
        callback_function = callback if events_handler is None else events_handler.callback
        self.channel.basic_consume(queue=queue_name,on_message_callback=lambda ch, method, properties, body: callback_function(ch, method, properties, body))
        threading.Thread(target=lambda: self.channel.start_consuming()).start()
        # thread = threading.Thread(target=self.channel.start_consuming)
        # thread.start()
        # thread.join()

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def fetch_new_event_payload(self):
        return {
            "event":None,
            "payload":{}
        }
    
    def put_on_bus_events(self,data):
        type_of_exchange='fanout'
        self.set_exchange(exchange=bus_events_exchange,exchange_type=type_of_exchange)
        self.channel.basic_publish(exchange=bus_events_exchange, routing_key='', body=json.dumps(data))
        print(f"Event {data['event']} published to bus events")

        
    

    

