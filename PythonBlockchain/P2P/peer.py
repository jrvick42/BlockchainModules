import pickle
import socket
import sys
import time
import threading
from uuid import uuid4
import os
from os import system, name
from subprocess import call
from datetime import datetime
import traceback
import pprint

# Custom Imports
from wallet import Wallet
from contacts import ContactList
from blockchain import Blockchain

# Price of 1 kW
PRICE = 1


class Peer():
    def __init__(self):

        # Define the data and variables that will be used by the Peer
        self.profile = {'id': None, 'username': None, 'addr': None,
                        'port': None, }     # This Peer's Info
        self.contacts = ContactList()       # Contact List
        self.blockchain = Blockchain()      # Blockchain
        self.wallet = Wallet()              # Wallet
        self.battery = Wallet(currency='kW')  # Battery Bank
        self.listen_port = 0                # Where to contact this Peer

        self.notifications = []

        self.awaitingValidation = True
        self.validated = False

    def serverGo(self):
        self.server = PeerServer(kwargs={'contacts': self.contacts,
                                         'blockchain': self.blockchain,
                                         'wallet': self.wallet,
                                         'port': self.listen_port,
                                         'profile': self.profile,
                                         'notifications': self.notifications, })

    def clientGo(self):
        self.client = PeerClient(kwargs={'contacts': self.contacts,
                                         'blockchain': self.blockchain,
                                         'wallet': self.wallet,
                                         'port': self.listen_port,
                                         'profile': self.profile,
                                         'notifications': self.notifications,
                                         'awaitFlag': self.awaitingValidation,
                                         'validatedFlag': self.validated})

    def register(self):
        self.client.register("127.0.0.1", 10000)

    def updateContacts(self, contacts):
        self.contacts = contacts

    def getPort(self):
        self.listen_port = self.server.getPort()

    def checkWallet(self):
        return self.wallet.getBalance()

    def checkBattery(self):
        return self.battery.getBalance()

    def startMenu(self):
        try:

            res = ""
            # Clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')

            while True:

                print("1. Contacts")
                print("2. Start Transaction")
                print("3. Check Wallet")
                print("4. Check Battery")
                print("5. Check Blockchain")
                print("6. Notifications", len(self.notifications))
                print("7. Exit\n")
                if res != "":
                    if 'hash' in res:
                        print("*** CURRENT BLOCKCHAIN ***\n")
                        pprint.pprint(res)
                    else:
                        print(res)
                    print()
                choice = input("Select: ")

                print()

                if choice == '1':

                    res = "*** CONTACTS ***\n"
                    res += str(self.contacts.all())

                elif choice == '2':

                    generating_transaction = False
                    while not generating_transaction:
                        # Clear the screen
                        os.system('cls' if os.name == 'nt' else 'clear')

                        print("Transaction Generator")
                        print("1. Buy Energy")
                        print("2. Sell Energy")
                        print("3. Cancel")
                        print()

                        t_choice = input("Select: ")

                        if t_choice == '1':
                            # Clear the screen
                            os.system('cls' if os.name ==
                                      'nt' else 'clear')

                            amount = int(
                                input("How much energy (kW) do you wish to purchase: "))
                            transaction = {'type': 'buy', 'amount': amount}
                            if self.startTransaction(transaction):
                                res = 'Transaction Completed'
                            else:
                                res = 'Transaction could not be completed. Try again ...'

                            generating_transaction = True
                        elif t_choice == '2':
                            # Clear the screen
                            os.system('cls' if os.name == 'nt' else 'clear')

                            amount = int(
                                input("How much energy (kW) do you wish to sell: "))
                            transaction = {'type': 'sell', 'amount': amount}
                            if self.startTransaction(transaction):
                                res = 'Transaction Completed'
                            else:
                                res = 'Transaction could not be completed. Try again ...'

                            generating_transaction = True
                        elif t_choice == '3':
                            print("Tansaction Cancelled")
                            generating_transaction = True

                        else:
                            print("Not a valid choice. Try again ...")
                            pass

                elif choice == '3':
                    res = "*** WALLET BALANCE ***\n"
                    res += "Balance\t" + str(self.checkWallet())

                elif choice == '4':
                    res = "*** BATTERY BALANCE ***\n"
                    res += "Balance\t" + str(self.checkBattery())

                elif choice == '5':

                    res = str(self.blockchain.chain)

                elif choice == '6':

                    res = "*** NOTIFICATIONS ***\n"
                    for n in self.notifications:
                        res += str(n) + "\n"

                    self.notifications = []

                elif choice == '7':
                    res = "BYE\n"
                    exit()

                # Clear the screen
                os.system('cls' if os.name == 'nt' else 'clear')

                pass
        except Exception as e:
            print(e)
            exit()

    def startTransaction(self, transaction):
        # check which type of transaction
        if transaction['type'] == 'buy':
            # Check that the Peer has the funding for the purchase
            # NOTE: Hardcoded price
            total_cost = transaction['amount'] * PRICE
            if total_cost > self.wallet.getBalance():
                self.notifications.append(datetime.now().strftime(
                    "%H:%M:%S") + "\tInsufficient funds for this purchase")
                return False
            else:
                # Create the block with the new transaction
                self.blockchain.add_transaction(
                    str(self.profile['username']), 'Smart Grid', total_cost, transaction['amount'])
                self.blockchain.add_block()

                # Propose the block with the new transaction
                self.client.propose()

                # Ensure we do not proceed until validation has been completed
                while self.client.validationStatus():
                        print("Client Awaiting Validation")
                        time.sleep(1)

                if self.client.isValidated():
                    # If all is in order, Carry out the transaction
                    self.wallet.withdrawal(total_cost)
                    self.battery.deposit(transaction['amount'])

                self.validated = False
                self.awaitingValidation = True

            return True
        elif transaction['type'] == 'sell':
            # Check that the Peer has the energy for the transaction
            # NOTE: Hardcoded price
            total_cost = transaction['amount'] * PRICE
            if transaction['amount'] > self.battery.getBalance():
                self.notifications.append(datetime.now().strftime(
                    "%H:%M:%S") + "\tInsufficient energy for this transaction")
                return False
            else:
                # Create the block with the new transaction
                self.blockchain.add_transaction(
                    str(self.profile['username']), 'Smart Grid', total_cost, transaction['amount'])
                self.blockchain.add_block()

                # Propose the block with the new transaction
                self.client.propose()

                # Ensure we do not proceed until validation has been completed
                while self.client.validationStatus():
                        print("Client Awaiting Validation")
                        time.sleep(1)

                if self.client.isValidated():
                    # If all is in order, Carry out the transaction
                    self.wallet.deposit(total_cost)
                    self.battery.withdrawal(transaction['amount'])

                self.validated = False
                self.awaitingValidation = True

            return True
        else:
            return False


class PeerServer(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):

        super().__init__(group=group, target=target, name=name)

        self.args = args
        self.contacts = kwargs['contacts']
        self.blockchain = kwargs['blockchain']
        self.wallet = kwargs['wallet']
        self.listen_port = kwargs['port']
        self.profile = kwargs['profile']
        self.notifications = kwargs['notifications']
        self.started = False
        return

    def run(self):

        # Setup the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = "127.0.0.1"
        self.listen_port = 10001

        # Attempt to start the socket until successful
        while not self.started:

            if self.listen_port < 65535:
                try:
                    self.sock.bind((hostname, self.listen_port))
                    self.sock.listen(1)
                    self.started = True
                except Exception as e:
                    self.notifications.append(
                        datetime.now().strftime("%H:%M:%S") + "\t" + str(e))
                    self.listen_port += 1
            else:

                print("Unable to start the Peer Server on any port")
                exit()

        # print("Listening on port:", str(self.listen_port))

        # Update this Peers profile
        self.profile['addr'] = hostname
        self.profile['port'] = self.listen_port

        # Wait for connections and pass the reqests onto the message handler
        while True:
            (client, addr) = self.sock.accept()
            self.notifications.append(datetime.now().strftime(
                "%H:%M:%S") + "\tConnection from " + str(addr))

            try:
                msg = client.recv(4098).decode()
                self.message_handler(client, msg)
            except Exception as e:
                print(str(type(e).__name__), e)
                pass

    def message_handler(self, c, m):
        if m == "introduction":

            # Let the Peer know we are ready
            c.send('ready'.encode())
            time.sleep(0.1)

            # Receive the Peers information
            info = pickle.loads(c.recv(2048))

            # Now we can add them as a contact
            self.contacts.addContact(
                info['id'], info['username'], info['addr'], info['port'])

            # let the Peer know we are done
            c.send('added'.encode())
            time.sleep(0.1)
            
            new_contact = self.contacts.all()[list(self.contacts.all().keys())[-1]]
            self.notifications.append(
                datetime.now().strftime("%H:%M:%S") + "\tNew contact has been added: %s" % new_contact)

        elif m == 'propose':

            c.send('ready'.encode())
            time.sleep(0.1)

            # print("MADE IT TO PROPOSE")
            block = pickle.loads(c.recv(8192))
            isValid = self.blockchain.validateProposal(block)

            if isValid:
                c.send('valid'.encode())
            else:
                c.send('not valid'.encode())
        elif m == 'validated':

            block = pickle.loads(c.recv(1024 * self.blockchain.length()))
            self.blockchain.appendBlock(block)
            self.notifications.append(
                datetime.now().strftime("%H:%M:%S") + "\tBlockchain has been updated!")


        else:
            res = m + " : Is not a valid request"
            c.send(res.encode())

    def getPort(self):
        while not self.started:
            time.sleep(1)
        return self.listen_port


class PeerClient(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):

        super().__init__(group=group, target=target, name=name)

        self.args = args
        self.contacts = kwargs['contacts']
        self.blockchain = kwargs['blockchain']
        self.wallet = kwargs['wallet']
        self.listen_port = kwargs['port']
        self.profile = kwargs['profile']
        self.notifications = kwargs['notifications']
        self.awaitingValidation = kwargs['awaitFlag']
        self.validated = kwargs['validatedFlag']

        return

    def run(self):
        print("Peer Client Starting ...")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def register(self, addr, port):
        print("Peer starting registration ...")
        self.sock.connect((str(addr), port))
        self.sock.send("register".encode())
        time.sleep(0.1)

        # Wait for registrar to become ready for our information
        res = self.sock.recv(1024).decode()
        if res == 'readyForInfo':
            username = input("Enter your username: ")
            uuid = uuid4()
            user_information = {
                'id': uuid, 'username': username, 'addr': addr, 'port': self.listen_port}
            self.sock.send(pickle.dumps(user_information))
            time.sleep(0.1)

            # Lastly, we can update this Peers info
            self.profile['id'] = uuid
            self.profile['username'] = username

        else:
            print("Something went wrong. Try to register again ...")
            # Close the connection to the Registrar
            # self.sock.shutdown()
            self.sock.close()
            exit()

        # Await a response from the registrar
        msg = self.sock.recv(1024).decode()
        time.sleep(0.1)

        # If we are the only client, there is nothing to do but start the Main Menu
        if msg == "only client":
            self.notifications.append(datetime.now().strftime(
                "%H:%M:%S") + "\tNo peers on the network")

        elif msg == "update contacts":
            self.contacts.updateContacts(pickle.loads(self.sock.recv(4096)))
            self.notifications.append(datetime.now().strftime(
                "%H:%M:%S") + "\tReceived the current client list")

        # Get the starting blockchain from the registrar
        chain = pickle.loads(self.sock.recv(2048))
        time.sleep(0.1)
        self.blockchain.updateChain(chain)

        # Close the connection to the Registrar
        # self.sock.shutdown()
        self.sock.close()

    def introduce(self):

        # For each of the contacts in our contact list,
        # connect to their server and introduce yourself

        for key in self.contacts.all().keys():

            # Create a new socket since the original was closed
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            contact = self.contacts.all()[str(key)]

            self.sock.connect((str(contact[1]), int(contact[2])))

            # If they are ready, send your request
            self.sock.send('introduction'.encode())
            time.sleep(0.1)

            res = self.sock.recv(1024).decode()
            if res == "ready":

                # Now send the actual data
                self.sock.send(pickle.dumps(self.profile))
                time.sleep(0.1)

                # Check that the Peer added your information
                if self.sock.recv(1024).decode() == "added":

                    # Intro successful, close connection
                    self.notifications.append(
                        datetime.now().strftime("%H:%M:%S") + "\tIntrodution to %s successful" % contact[0])

                    # self.sock.shutdown()
                    self.sock.close()

                else:
                    self.notifications.append(
                        datetime.now().strftime("%H:%M:%S") + "\tError during introduction to %s" % contact[0])

            else:
                print("Peer is unready. Try again later ...")
                # Close the connection to the Registrar
                # self.sock.shutdown()
                self.sock.close()
                exit()

            # End our socket. StartMain will create a new one
            self.sock.close()

    def propose(self):

        # check if we are the only peer
        if len(self.contacts.all().keys()) == 0:
            self.validated = True
            self.awaitingValidation = False

        votes_for = 0

        # Broadcast the proposal to all of the Peers for validation
        for key in self.contacts.all().keys():
            contact = self.contacts.all()[str(key)]
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(contact[1]), int(contact[2])))

            self.sock.send('propose'.encode())
            time.sleep(0.1)

            response = self.sock.recv(1024).decode()

            if response == 'ready':

                b = self.blockchain.get_last_block()

                self.sock.send(pickle.dumps(b))
                time.sleep(0.1)

                res = self.sock.recv(1024).decode()


                if res == 'valid':
                    votes_for += 1
                elif res == 'not valid':
                    self.notifications.append(datetime.now().strftime(
                        "%H:%M:%S") + "\tProposed block could not be verified by %s" % contact[0])

                self.sock.close()

        # Do we have enough votes to validate the block
        if votes_for == len(self.contacts.all().keys()):
            # send the verified block to each peer
            for key in self.contacts.all().keys():
                contact = self.contacts.all()[str(key)]
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((str(contact[1]), int(contact[2])))
                self.sock.send('validated'.encode())
                time.sleep(0.1)
                self.sock.send(pickle.dumps(self.blockchain.get_last_block()))
                self.sock.close()

                self.validated = True
                self.awaitingValidation = False

            self.notifications.append(datetime.now().strftime(
                "%H:%M:%S") + "\tBlock added successfully!")
        else:
            # block is not validated
            # print("BLOCK COULD NOT BE VALIDATED")
            self.blockchain.pop()
            self.notifications.append(datetime.now().strftime(
                "%H:%M:%S") + "\tBlock could not be added. Try Again ...")

        self.awaitingValidation = False

    def validationStatus(self):
        return self.awaitingValidation

    def isValidated(self):
        return self.validated

if __name__ == "__main__":

    peer = Peer()

    # Start the Peer Server
    peer.serverGo()
    peer.server.daemon = True
    peer.server.start()

    # Wait for the server to start and update the client with its info
    peer.getPort()

    # Start the Peer Client
    peer.clientGo()
    peer.client.start()
    time.sleep(1)
    peer.client.register('127.0.0.1', 10000)

    # Introduce yourslef to the rest of the network
    peer.client.introduce()

    # Start the Client Menu
    peer.startMenu()
