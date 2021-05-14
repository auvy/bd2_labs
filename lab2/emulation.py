import ops.connection as redis

redis.connect()
rconnection = redis.connection

from ops.user import User
from ops.message import Message

from threading import Thread
from faker import Faker
from random import randint
import atexit

class Emulation(Thread):
    def __init__(self, name, users):
        Thread.__init__(self)
        self.conn = rconnection
        self.name = name
        self.users = users
        self.user_id = User.register(name)

    def run(self):
        for i in range(amount):
            sentence = fake.sentence(nb_words=5, variable_nb_words=True, ext_word_list=None)
            receiver = users[randint(0, amount - 1)]
            print(f"Message {sentence} was sent to {receiver}");
            Message.create_message(self.user_id, sentence, receiver)

def exit():
    online = rconnection.smembers("online")
    for i in online:
        rconnection.srem("online", i)
        rconnection.publish("logout", f"User {i} signed out.")
        print(f"{i} exits app. Have a good day!")

if __name__ == '__main__':
    fake = Faker()
    atexit.register(exit)
    amount = 5
    
    users = [fake.profile(fields=["username"], sex=None)["username"] for user in range(amount)]
    threads = []

    for i in range(amount):
        print(f"User: {users[i]}")
        threads.append(Emulation(users[i], users))

    for t in threads:
        t.start()