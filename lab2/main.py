import os
import logging
from pathlib import Path

from ops.user import User
from ops.message import Message

import ops.connection as redis
redis.connect()
rconnection = redis.connection

import re


FILE = os.path.join(os.path.dirname(Path(__file__).absolute()), 'logs.txt')
logging.basicConfig(filename="logs.txt", level=logging.INFO)

def start_menu():
    print("\nMAIN MENU")
    print("1. Register")
    print("2. Login")
    print("0. Exit")
    return int(input("Enter the number of action: "))

def user_menu(uid):
    print(f"\nUSER MENU: {User.get_username(uid)}")
    print("1. Inbox")
    print("2. Write new message")
    print("3. Message status")
    print("4. Give admin")
    print("0. Logout")
    return int(input("Enter the number of action: "))

def main():
    while True:
        action = start_menu()

        #register
        if action == 1:
            username = input("Enter new username: ")
            uid = User.register(username)
            
            if User.is_logged_in(uid):
                user(uid)
        #login
        elif action == 2:
            username = input("Enter username: ")
            uid = User.login(username)
            
            if User.is_logged_in(uid):
                user(uid)
        #exit
        elif action == 0:
            print("Farewell!")
            break
        #wrong choice
        else:
            print("Enter correct choice (num 0 to 2): ")

def admin_menu(uid):
    print(f"\nADMIN MENU: {User.get_username(uid)}")
    print("1. Sender rating")
    print("2. Spammer rating")
    print("3. View logs")
    print("4. Users online")
    print("0. Exit")
    return int(input("Enter the number of action: "))

def user(uid):
    while True:
        action = user_menu(uid)

        #inbox
        if action == 1:
            Message.get_inbox(uid)
        #new message
        elif action == 2:
            text = input("Enter message: ")
            receiver = input("Enter username of the receiver: ")
            
            if Message.create_message(uid, text, receiver):
                print(f"Sent message to {receiver}!")
            else:
                print("Got some trouble with sending a message")
        #message status
        elif action == 3:
            keys = ["queue", "checking", "blocked", "sent", "delivered"]
            view = ["Queued", "Checking", "Blocked", "Sent", "Delivered"]

            user = rconnection.hmget(f"user{uid}", keys)
            
            for i in range(5):
                print(f"-{view[i]}: {user[i]}")
                
        #get admin
        elif action == 4:
            return admin(uid)
        #logout
        elif action == 0:
            User.logout(uid)
            break
        #incorrect
        else:
            print("Enter correct choice (num 0 to 4): ")


def admin(uid):
    while True:
        action = admin_menu(uid)

        #get senders
        if action == 1:
            quantity = 10
            active_senders = rconnection.zrange("sent", 0, quantity, desc=True, withscores=True)

            if len(active_senders) == 0:
                print("No senders found.")
            else:
                print(f"All {len(active_senders)} most active senders: ")
                for index, sender in enumerate(active_senders):
                    sid = re.search(r'\d+', sender[0]).group()
                    uname = User.get_username(sid)
                    print(f"{index + 1}. {uname} - {int(sender[1])} messages")
        #get spammers
        elif action == 2:
            quantity = 10
            active_spamers = rconnection.zrange("spam", 0, quantity, desc=True, withscores=True)

            if len(active_spamers) == 0:
                print("No spamers found.")
            else:
                print(f"All {len(active_spamers)} most active spamers: ")
                for index, sender in enumerate(active_spamers):
                    sid = re.search(r'\d+', sender[0]).group()
                    uname = User.get_username(sid)
                    print(f"{index + 1}. {uname} - {int(sender[1])} messages")
        #get logs
        elif action == 3:
            try:
                with open(FILE) as file:
                    print(file.read())
            except Exception as e:
                return f"Error: Log reading: '{e}'"
        #online members
        elif action == 4:
            online_users = rconnection.smembers("online")
            if len(online_users) == 0:
                print("No one's around.")
            else:
                print(f"{len(online_users)} users online: ")
                for user in online_users:
                    print(f"-{user}")
        #logout
        elif action == 0:
            print(f"Farewell, {User.get_username(uid)}!")
            break
        #incorrect
        else:
            print("Enter correct choice (num 0 to 4): ")

if __name__ == '__main__':
    main()
