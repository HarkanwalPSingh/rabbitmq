import pika
import time
import threading
from logger import Logger

CONSUMER_DELAY = 5
# CONSUMER_TIMEOUT = 30

log = Logger('consumer_factory').getLogger('INFO')

class RabbitMQConsumer(threading.Thread):
    def __init__(self, queue_name):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.queue_name = queue_name
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name, auto_delete=False)
        # self.channel.queue_bind(queue=queue_name, exchange='', routing_key=queue_name) # No need to bind in default exchange
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.handle_message)
        threading.Thread(target=self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.handle_message))

    def handle_message(self, channel, method, properties, body):
        log.info(f"{self.queue_name} consumer received {body}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(CONSUMER_DELAY)
    
    def run(self):
        log.info(f"Starting new consumer for {self.queue_name}")
        self.channel.start_consuming()
    
if __name__ == '__main__':
    for i in range(10):
        print(f'Thread: {i}')
        consumer = RabbitMQConsumer(queue_name=f"queue-{i}")
        consumer.start()
