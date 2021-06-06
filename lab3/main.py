from ops.neo4 import neo4j
import os
import emulation as emul
from ops.tag import Tag 

def start_menu():    
    print("MAIN MENU")
    print("1. Launch emulation")
    print("2. Users with tag set")
    print("3. User pairs with N relation")
    print("4. Path between 2 users")
    print("5. Spammer pairs")
    print("6. Unrelated user list with tag set")
    print("0. Exit")
    return int(input("Enter the number of action: "))

def main():
    while True:
        action = start_menu()

        if action == 1:
            os.system('python3 emulation.py')
            print("Emulation completed!\n")

        elif action == 2:
            enums = list(map(lambda c: c.value, Tag))
            newlist = list()
            res = ''
            for e in enums:
                while True:
                    res = input(f'Have "{e[1]}" tag? y or n: ')
                    if res == 'y':
                        newlist.append(e[1].lower())
                        break
                    elif res == 'n':
                        break
                    
            users = neo4j.get_related_u_by_tags(newlist)
            print(f"Users: ")
            iter = 1
            for user in users:
                print(f"{iter}. {user}")
                iter += 1

        elif action == 3:
            n = int(input("Enter length of relations: "))
            users = neo4j.get_u_with_n_relation(n)
            print("User pairs: ")
            iter = 1
            for user in users:
                print(f"{iter}. {user[0]} - {user[1]}")
                iter += 1

        elif action == 4:
            username1 = input("Enter username1: ")
            username2 = input("Enter username2: ")
            way = neo4j.shortest_way(username1, username2)
            text = ""
            print("Shortest path: ")
            for step in way:
                text += f"{step} -> "
            print(text[:-3])

        elif action == 5:
            spammers = neo4j.get_spammer_u()
            print("Spammer pairs: ")
            iter = 1
            for user in spammers:
                print(f"{iter}. {user[0]} - {user[1]}")
                iter += 1

        elif action == 6:
            enums = list(map(lambda c: c.value, Tag))
            newlist = list()
            res = ''
            for e in enums:
                while True:
                    res = input(f'Have "{e[1]}" tag? y or n: ')
                    if res == 'y':
                        newlist.append(e[1].lower())
                        break
                    elif res == 'n':
                        break
            unrelated_users = neo4j.get_u_with_tags(newlist)
            print("Messages: ")
            iter = 1
            for user in unrelated_users:
                print(f"{iter}. {user[0]}")
                iter += 1

        elif action == 0:
            print("Farewell!")
            break

        else:
            print("Enter correct choice (num 0 to 4): ")


if __name__ == '__main__':
    main()