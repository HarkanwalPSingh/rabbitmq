import pika
import random
import string

# EXCHANGE = "events"

class SendMessage:
    def __init__(self) -> None:
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.conn.channel()
        # channel.queue_declare(queue=queue, auto_delete=False)
    
    def publish_message(self, queue, message):
        self.channel.queue_declare(queue=queue, auto_delete=False)
        # self.channel.queue_bind(queue=queue_name, exchange=EXCHANGE, routing_key=queue_name) # No need to bind in default exchange
        self.channel.basic_publish(exchange='', routing_key=queue, body=f'Message: {message}')

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    message_sender = SendMessage()
    # Send messages for testing purpose
    for i in range(100):
        random_queue = f"queue-{random.randint(0,9)}"
        random_message = ''.join(random.choices(string.ascii_letters, k=10))
        message_sender.publish_message(random_queue, random_message)