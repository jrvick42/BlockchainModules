import threading
import socket
import sys
import time
import pickle
from uuid import uuid4

# Custom Imports
from contacts import ContactList
from blockchain import Blockchain


class Registrar():

    def __init__(self, address, port):

        self.registered_peers = ContactList()
        self.numPeers = 0
        self.registrar = self.startRegistrar(address, port)
        self.cont = True
        self.blockchain = Blockchain()

    def startRegistrar(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((address, int(port)))
        sock.listen(100)
        return sock

    def getRegistrar(self):
        print("Successful creation of the Registrar")
        return self.registrar

    def addContact(self, username, uid, address, port):
        self.registered_peers.addContact(
            str(uid), str(username), str(address), port)


def connectingThread(connection, address, t):
    print("\nClient connecting... Waiting on data...")
    request = connection.recv(1024).decode()
    if request == "register":
        print("Successful connection from {}".format(address))

        # Let our connection know we are ready to accept their informtion
        connection.send("readyForInfo".encode())
        time.sleep(0.1)

        # Accept the connections information
        res = pickle.loads(connection.recv(2048))
        time.sleep(0.1)

        if registrar.registered_peers.numContacts() == 0:
            connection.send("only client".encode())
            print("Informed connection that it is the first client")

        else:
            connection.send("update contacts".encode())
            time.sleep(0.1)
            sendContactList(connection)

        connection.send(pickle.dumps(t.blockchain.chain))

        # Once the clients contact list has been sent, update out contact list
        registrar.registered_peers.addContact(
            res['id'], res['username'], res['addr'], res['port'])

        if registrar.registered_peers.checkById(res['id']):
            print("Successfully added contact")
            print(registrar.registered_peers.all())
        else:
            print("Unknown error while updating contact list")

        return

    elif request == "kill_registrar":
        print("Recieved KillSIG from user. Ending Registrar Thread...")
        t.cont = False
        return


def sendContactList(connection):
    connection.send(pickle.dumps(registrar.registered_peers.all()))
    time.sleep(0.1)


# def send_chain(connection):
#     connection.send(pickle.dumps(Registrar.bc.chain))


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Proper Usage: registrar.py or python registrar.py")
        exit()

    # address = input("What IP would you like to run the Registrar on: ")
    # port = input("What port would you like to run the Registrar on: ")
    print("Starting Registrar on IP 127.0.0.1 and port 6789")
    global registrar
    global socket
    registrar = Registrar("127.0.0.1", 10000)
    socket = registrar.getRegistrar()

    while registrar.cont:
        conn, addr = socket.accept()
        connThread = threading.Thread(
            target=connectingThread, args=(conn, addr, registrar))
        connThread.start()
        connThread.join()
