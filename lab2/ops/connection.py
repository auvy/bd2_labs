import redis
import sys

class Redis:
    host = 'localhost'
    port = 6379

connection = redis.Redis(host=Redis.host, port=Redis.port, db=0, decode_responses=True)

def connect():
    try:
        connection.ping()
    except Exception as err:
        sys.exit(err)
    