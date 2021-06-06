import ops.connection as redis
import logging
import datetime
import ops.neo4 as neo4
logging.basicConfig(filename="logs.txt", level=logging.INFO)


redis.rconnect()
rconnection = redis.rconnection

class User: 
    def register(username):
        if rconnection.hget("users", username):
            print(f"{username} already exists.")
            return -1

        user_id = rconnection.incr("user_id")
        user_key = f"user{user_id}"
        user_info = {
            "id": user_id,
            "name": username,
            "queue": 0,
            "checking": 0,
            "blocked": 0,
            "sent": 0,
            "delivered": 0
        }

        rconnection.hset("users", username, user_id)
        for key in user_info.keys():
            rconnection.hset(user_key, key, user_info[key])

        rconnection.publish("register", f"User {username} registered")
        rconnection.sadd("online", username)


        neo4.neo4j.register(username, user_id)


        logging.info(f"({datetime.datetime.now()}): User {username} registered")
        return user_id

    def login(username):
        user_id = rconnection.hget("users", username)

        if not user_id:
            print(f"{username} does not exist. Register?")
            return -1

        rconnection.publish("login", f"User {username} logged in")
        rconnection.sadd("online", username)

        neo4.neo4j.login(user_id)

        logging.info(f"({datetime.datetime.now()}): User {username} logged in")
        return user_id

    def logout(user_id):
        username = User.get_username(user_id)
        rconnection.publish("logout", f"User {username} logged out")
        rconnection.srem("online", username)
        
        neo4.neo4j.logout(user_id)
        
        logging.info(f"({datetime.datetime.now()}): User {username} logged out")


    def get_username(user_id):
        return rconnection.hmget(f"user{user_id}", ["name"])[0]

    def is_logged_in(user_id):
        return user_id != -1