import ops.connection as redis
redis.connect()
rconnection = redis.connection

from ops.message import Message
from ops.user import User

from threading import Thread
from random import randint
import time
import random

import logging
import datetime
logging.basicConfig(filename="logs.txt", level=logging.INFO)



DELAY = randint(0, 2)

def is_spam():
    return random.random() > 0.5

class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        message = rconnection.brpop("queue")

        if message:
            message_id = message[1]
            message_key = f"message{message_id}"
            rconnection.hset(message_key, "status", "checking")

            message = rconnection.hmget(message_key, ["sender_id", "receiver_id"])
            sender_id = message[0]
            receiver_id = message[1]
            sender_name = User.get_username(sender_id)

            rconnection.hincrby(f"user{sender_id}", "queue", -1)
            print("Message enqueued")
            rconnection.hincrby(f"user{sender_id}", "checking", 1)
            time.sleep(DELAY)

            pipeline = rconnection.pipeline(True)
            pipeline.hincrby(f"user{sender_id}", "checking", -1)


            if is_spam():
                print(f"{sender_name} sent spam: id={message_id}")

                message_text = rconnection.hmget(message_key, ["text"])[0]
                logging.info(f"({datetime.datetime.now()}): User {sender_name} sent spam: {message_text}")

                pipeline.zincrby(f"spam", 1, f"user{sender_id}")
                pipeline.hset(message_key, "status", "blocked")
                pipeline.hincrby(f"user{sender_id}", "blocked", 1)
                pipeline.publish("spam", f"User {sender_name} sent spam: {message_text}.")
            else:
                print(f"Checked and sent message[{message_id}] from {sender_name}.")
                pipeline.hset(message_key, "status", "sent")
                pipeline.hincrby(f"user{sender_id}", "sent", 1)
                pipeline.sadd(f"sent_to:{receiver_id}", message_id)
            
            pipeline.execute()

def main():
    handlers = 5
    for i in range(handlers):
        worker = Worker()
        worker.daemon = True
        worker.start()

    while True:
        pass

if __name__ == '__main__':
    main()