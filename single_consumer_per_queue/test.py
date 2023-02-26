from consumer_factory import RabbitMQConsumer
from redis_db import RedisDB
from message import SendMessage
import random
import string
import time
from logger import Logger

log = Logger('test').getLogger('INFO')

redisDb = RedisDB()
messageSender = SendMessage()

def publish_message(queue_name, message):
    if redisDb.get_value(queue_name):
        # Don't start consumer if already running
        log.warn(f"Consumer for {queue_name} already running")
    else:
        # Start new consumer if not running
        # Mark the thread as Daemon thread that exits if the MainThread is terminated
        consumer = RabbitMQConsumer(queue_name=queue_name)
        consumer.setDaemon(True)
        consumer.start()
        redisDb.set_value(key=queue_name, value=1)

    # Send message to queue
    messageSender.publish_message(queue_name, message)

if __name__ == '__main__':
    for i in range(100):
        random_queue = f"queue-{random.randint(1,10)}"
        random_message = ''.join(random.choices(string.ascii_letters, k=10))
        publish_message(random_queue, random_message)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Flushing Reddis Keys and Closing Connection")
        redisDb.close()
        log.info("Redis Connection Closed")
        raise