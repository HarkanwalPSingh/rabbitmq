from single_consumer_per_queue.consumer_factory import RabbitMQConsumer
from redis_db import RedisDB
from message import SendMessage
import random
import string
from logging import getLogger, getLevelName, Formatter, StreamHandler

log = getLogger('test')
log.setLevel(getLevelName('INFO'))
log_formatter = Formatter("%(asctime)s [%(levelname)s] [%(threadName)s] %(name)s: %(message)s ") # I am printing thread id here
console_handler = StreamHandler()
console_handler.setFormatter(log_formatter)
log.addHandler(console_handler)

redisDb = RedisDB()
messageSender = SendMessage()

def publish_message(queue_name, message):
    if redisDb.get_value(queue_name):
        # Don't start consumer if already running
        log.warn(f"Consumer for {queue_name} already running")
    else:
        # Start new consumer if not running
        # print(f"Starting new consumer for {queue_name}")
        consumer = RabbitMQConsumer(queue_name=queue_name, timeout=5)
        consumer.start()
        redisDb.set_value(key=queue_name, value=1)

    # Send message to queue
    messageSender.publish_message(queue_name, message)

if __name__ == '__main__':
    
    try:
        for i in range(100):
            random_queue = f"queue-{random.randint(1,10)}"
            random_message = ''.join(random.choices(string.ascii_letters, k=10))
            publish_message(random_queue, random_message)
    except KeyboardInterrupt:
        log.info("Flushing Reddis Keys and Closing Connection")
        redisDb.close()
        log.info("Redis Connection Closed")



