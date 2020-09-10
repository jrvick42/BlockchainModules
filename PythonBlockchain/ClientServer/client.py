import pickle
import socket
import sys
import time
import threading
import pickle
from os import system, name
from subprocess import call

class PeerServer():
    def __init__(self):
        print("Peer Server Init")
    

class PeerClient():
    def __init__(self):
        print("Peer Client Init")

class Peer():
    def __init__(self):
        self.Username = ''
        self.uuid = None
        self.tracker = None
        self.blockchain = []
        self.inbox = []
        self.contacts = {}

    def setTracker(self, tracker):
        self.tracker = tracker

    def setContacts(self, contacts, ids):
        count = 0
        for i in contacts:
            self.contacts[str(i)] = ids[count]
            count += 1
        self.uuid = ids[-1]

    def updateChain(self, chain):
        self.blockchain = chain

    def checkContact(self, recipient):
        return recipient in self.contacts

    def set_name(self, name):
        self.Username = name

def connectToTracker():
    print(" Attempting to connect to IP 127.0.0.1 on port 6789")
    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(("127.0.0.1", 6789))
    print(" Connected to the Tracker successfully")
    tracker.send("connect".encode())
    time.sleep(0.1)
    response = tracker.recv(1024).decode()
    if response == "ready":
        tracker.send(peer.Username.encode())
        time.sleep(0.1)
        updatedContacts = pickle.loads(tracker.recv(2048))
        time.sleep(0.1)
        updatedIDs = pickle.loads(tracker.recv(2048))
        time.sleep(0.1)
        chain = pickle.loads(tracker.recv(2048))
        peer.setContacts(updatedContacts, updatedIDs)
        peer.updateChain(chain)
        tracker.close()

def new_transaction():
    while True:
        print()
        io_options = ["Power Withdrawal", "Power deposit", "Cancel Transaction"]
        for i in range(len(io_options)):
            print(" {}. {}".format(i + 1, io_options[i]))
        try:
            io_choice = input("\n Select a transaction type: ")
            if io_choice == "1":
                while True:
                    try:
                        w_choice = input("\n How many kWs would you like to order: ")
                        publishTransaction(True, w_choice)
                    except ValueError:
                        print("\n Please only use whole number answers")
                    return
            elif io_choice == "2":
                while True:
                    try:
                        d_choice = input("\n How many kWs would you like to deposit: ")
                        publishTransaction(False, d_choice)
                    except ValueError:
                        print("\n Please only use whole number answers")
                    return
            elif io_choice == "3":
                return -1
            else:
                print("\n Invalid Selection")
        except ValueError:
            print("\n Please use numbers for selection...")

def publishTransaction(io, amount):
    print(" Attempting to connect to Tracker")
    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(("127.0.0.1", 6789))
    print(" Connected successfully")
    tracker.send("new_transaction".encode())
    time.sleep(0.1)
    tracker.send(pickle.dumps([str(peer.uuid), str(io), str(amount)]))
    print(" Awaiting confirmation...")
    chain = pickle.loads(tracker.recv(2048))
    if chain:
        print(" Block added successfully")
        peer.updateChain(chain)
    else:
        print("Block not added successfully")

def kill_tracker():
    print(" Attempting to connect to IP 127.0.0.1 on port 6789")
    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(("127.0.0.1", 6789))
    print(" Connected to the Tracker successfully")
    tracker.send("kill_tracker".encode())
    time.sleep(0.1)
    response = tracker.recv(1024).decode()
    print(" Shutting down tracker")
    try:
        tracker.close()
    except:
        pass

def getChain():
    print(" Attempting to connect to IP 127.0.0.1 on port 6789")
    tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tracker.connect(("127.0.0.1", 6789))
    print(" Connected to the Tracker successfully")
    tracker.send("update_blockchain".encode())
    time.sleep(0.1)
    chain = pickle.loads(tracker.recv(2048))
    print(" Acquired most recent blockchain...")
    try:
        peer.updateChain(chain)
        tracker.close()
    except:
        pass

def show_contacts():
    return peer.contacts

def displayMainMenu():
    options = ["Create Transaction", "View Blockchain", "Request Updated Blockchain", "View Contact List", "Exit"]
    print()

    for i in range(len(options)):
        print(" {}. {}".format(i+1, options[i]))
    try:
        choice = input("\n Select an option: ")
    except ValueError:
        print(" Please use numbers for selection...")

    if choice == "1":
        clear()
        if new_transaction() == -1:
            clear()
            print()
            print(" Transaction Canceled")
            return False
            clear()
        print()
        print(" Transaction Completed")
        return False
    elif choice == "2":
        clear()
        print()
        print(peer.blockchain)
        return False
    elif choice  == "3":
        clear()
        getChain()
        print()
        print(peer.blockchain)
        return False
    elif choice == "4":
        clear()
        print()
        print(show_contacts())
        return False
    elif choice == "5":
        clear()
        return True
    elif choice == "0":
        kill_tracker()
        clear()
        return True
    else:
        print(" Not a valid option")

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def main(argv):
    global peer
    peer = Peer()
    peer.set_name(input(" What is your username: "))
    connectToTracker()
    exit = False
    while not exit:
        exit = displayMainMenu()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(" Proper Usage: peer.py or 'python peer.py'")
        exit()
    main(sys.argv)
