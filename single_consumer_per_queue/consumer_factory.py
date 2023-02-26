import pika
import time
import threading
from logging import getLogger, getLevelName, Formatter, StreamHandler

TIMEOUT = 5

# Setting Logger
log = getLogger('consumer_factory')
log.setLevel(getLevelName('INFO'))
log_formatter = Formatter("%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s ")
console_handler = StreamHandler()
console_handler.setFormatter(log_formatter)
log.addHandler(console_handler)

class RabbitMQConsumer(threading.Thread):
    def __init__(self, queue_name, timeout):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.queue_name = queue_name
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name, auto_delete=False)
        # self.channel.queue_bind(queue=queue_name, exchange='', routing_key=queue_name) # No need to bind in default exchange
        self.timeout = TIMEOUT
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.handle_message)
        threading.Thread(target=self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.handle_message))

    def consume(self):
        self.channel.start_consuming()

    def handle_message(self, channel, method, properties, body):
        log.info(f"{self.queue_name} consumer received {body}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        time.sleep(self.timeout)
    
    def run(self):
        print(f"Starting new consumer for {self.queue_name}")
        self.channel.start_consuming()

if __name__ == '__main__':
    for i in range(10):
        print(f'Thread: {i}')
        consumer = RabbitMQConsumer(queue_name=f"queue-{i}", timeout=5)
        consumer.start()
