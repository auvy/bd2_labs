from ops.tag import Tag
from os import pipe
import ops.connection as redis
import ops.tag as tag
redis.rconnect()
rconnection = redis.rconnection
from ops.user import User

import ops.neo4 as neo4


import random

class Message:
    def create_message(user_id, message, receiver, tags):
        message_id = rconnection.incr("message_id")
        receiver_id = rconnection.hget("users", receiver)
        if not receiver_id:
            print(f"{receiver} does not exist, can't send a message.")
            return False


        message_key = f"message{message_id}"
        message_info = {
            "id": message_id,
            "text": message,
            "sender_id": user_id,
            "receiver_id": receiver_id,
            "status": "created",
            "tags": ",".join(tags)
        }

        pipeline = rconnection.pipeline(True)

        for key in message_info.keys():
            pipeline.hset(message_key, key, message_info[key])

        pipeline.lpush("queue", message_id)
        pipeline.hset(message_key, "status", "queue")

        pipeline.hincrby(f"user{user_id}", "queue", 1)
        pipeline.zincrby("sent", 1, f"user{user_id}")

        pipeline.execute()

        neo4.neo4j.create_message(user_id, receiver_id, {"id": message_id, "tags": tags})

        return message_id

    def get_inbox(user_id):
        messages = rconnection.smembers(f"sent_to{user_id}")

        if len(messages) == 0:
            print("No messages")
            return

        for message_id in messages:
            message = rconnection.hmget(f"message{message_id}", ["text", "status", "sender_id"])

            if message[1] != "delivered":
                rconnection.hset(f"message{message_id}", "status", "delivered")
                rconnection.hincrby(f"user{message[2]}", "sent", -1)
                rconnection.hincrby(f"user{message[2]}", "delivered", 1)

            print(f"{message[0]} -> FROM: {User.get_username(message[2])}")