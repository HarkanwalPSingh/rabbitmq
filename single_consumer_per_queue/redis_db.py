from redis import Redis

class RedisDB:
    def __init__(self) -> None:
        self.conn = Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

    def set_value(self, key, value):
        self.conn.set(key, value)

    def get_value(self, key):
        return self.conn.get(key)
    
    # Flush all keys and close connection
    def close(self):
        self.conn.flushdb()
        self.conn.close()

if __name__ == '__main__':
    redis_db = RedisDB()
    print(redis_db.get_value("queue-1"))
    
