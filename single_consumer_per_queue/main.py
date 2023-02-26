import os, sys
from single_consumer_per_queue.consumer_factory import RabbitMQConsumer
from redis_db import RedisDB
from message import SendMessage

def send_message(redisDb, sendMessage):

    while True:
        # user_input = input("Enter Queue Name and Value:\n")
        user_input = input("\n")
        args = user_input.split()
        if len(args) == 2:
            queue_name = args[0]
            message = args[1]

            if redisDb.get_value(queue_name):
                # Don't start consumer if already running
                print(f"Consumer for {queue_name} already running")
            else:
                # Start new consumer if not running
                # print(f"Starting new consumer for {queue_name}")
                consumer = RabbitMQConsumer(queue_name=queue_name, timeout=5)
                consumer.start()
                redisDb.set_value(key=queue_name, value=1)
            
            # Send message to queue
            sendMessage.send_message(queue_name, message)

        else:
            print("Enter only two arguments")

if __name__ == '__main__':
    try:
        print("Enter Queue Name and Value")
        redisDb = RedisDB()
        sendMessage = SendMessage()
        send_message(redisDb, sendMessage)
    except KeyboardInterrupt:
        print('Interrupted')
        # Close connections
        redisDb.close()
        print('INFO: Closed Redis Connection')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)