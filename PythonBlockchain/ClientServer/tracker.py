import threading
import socket
import sys
import time
import pickle
import blockchain
from uuid import uuid4


class Tracker():

    def __init__(self, address, port):
        self.connectedUsernames = ["Smart Grid"]
        self.connectedIDs = [str(uuid4())]
        self.connectedAddresses = ["127.0.0.1"]
        self.connectedPorts = ["6789"]
        self.numPeers = 0
        self.tracker = self.startTracker(address, port)
        self.bc = blockchain.Blockchain()
        self.cont = True

    def startTracker(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((address, int(port)))
        sock.listen(100)
        return sock

    def getTracker(self):
        print("Successful creation of the Tracker")
        return self.tracker

    def addContact(self, username, uid, address, port):
        self.connectedUsernames.append(str(username))
        self.connectedIDs.append(str(uid))
        self.connectedAddresses.append(str(address))
        self.connectedPorts.append(str(port))

def connectingThread(connection, address, t):
    print("\nClient connecting... Waiting on data...")
    request = connection.recv(1024).decode()
    if request == "connect":
        print("Successful connection from {}".format(address))

        connection.send("ready".encode())
        time.sleep(0.1)
        username = connection.recv(1024).decode()

        ip = str(address).split("'")[1]
        port = str(address).split(",")[1].strip(" ").strip(")")

        tracker.addContact(username, str(uuid4()), ip, port)

        sendContactList(connection)
        time.sleep(0.1)

        send_chain(connection)

        return

    elif request == "new_transaction":
        tx_data = pickle.loads(connection.recv(2048))
        t.bc.add_transaction(tx_data[0], t.connectedIDs[0], tx_data[2])
        t.bc.add_block()
        send_chain(connection)
        return
    elif request == "update_blockchain":
        send_chain(connection)
        return
    elif request == "kill_tracker":
        print("Recieved KillSIG from user. Ending Tracker Thread...")
        t.cont = False
        return

def sendContactList(connection):
    connection.send(pickle.dumps(tracker.connectedUsernames))
    time.sleep(0.1)
    connection.send(pickle.dumps(tracker.connectedIDs))

def send_chain(connection):
    connection.send(pickle.dumps(tracker.bc.chain))


def main():
    # address = input("What IP would you like to run the Tracker on: ")
    # port = input("What port would you like to run the Tracker on: ")
    print("Starting Tracker on IP 127.0.0.1 and port 6789")
    global tracker
    global socket
    tracker = Tracker("127.0.0.1", 6789)
    socket = tracker.getTracker()

    while tracker.cont:
        conn, addr = socket.accept()
        connThread = threading.Thread(target = connectingThread, args=(conn, addr, tracker))
        connThread.start()
        connThread.join()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Proper Usage: Tracker.py or python tracker.py")
        exit()
    main()
