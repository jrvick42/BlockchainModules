import hashlib
import json

import time
from uuid import uuid4


class Blockchain():

    def __init__(self):
        # Create the chain and transactions list
        self.chain = []
        self.transactions = []
        self.diff = 1

        # Create the genesis block
        self.add_block()

    def appendBlock(self, block):
        self.chain.append(block)

    def add_block(self):

        hash = ""
        p_hash = ""
        if len(self.chain) == 0:
            p_hash = "0"
        else:
            p_hash = str(self.chain[len(self.chain) - 1]["hash"])
        nonce = 0

        #####################################################################
        # Mine the block here. Each block will contain a single transaction #
        #####################################################################

        while True:
            t = time.time()
            digest = p_hash + str(self.transactions) + \
                str(t) + str(nonce) + str(self.diff)
            hash = hashlib.sha256(digest.encode()).hexdigest()
            if hash[:self.diff] == "0" * self.diff:
                break
            else:
                nonce += 1

        # Create the new block
        new_block = {
            'hash': hash,                # The hash of the new block
            'p_hash': p_hash,            # The hash of the previous block
            'tx': self.transactions,     # The list of current transactions
            'time': t,                   # The current time
            'nonce': nonce,              # The nonce needed to validate the block
            'difficulty': self.diff,     # The difficulty that was used while mining the block
        }

        # Reset the list of transactions
        self.transactions = []

        # Add the block to the chain
        self.chain.append(new_block)

    def add_transaction(self, send, recv, cost, amount):

        ##############################################################
        # Here is where we will send the transaction to be verified #
        ##############################################################

        # Get the current size of the transaction list
        current_size = len(self.transactions)

        # Add the new transaction
        self.transactions.append({
            'sender': send,
            'reciever': recv,
            'cost': cost,
            'amount': amount,
            'time': time.time()
        })

        # Chech that the transaction was added successfully and return
        if(current_size != len(self.transactions) - 1):
            return False
        return True

    def validateProposal(self, block):
        digest = str(block['p_hash']) + str(block['tx']) + \
            str(block['time']) + str(block['nonce']) + str(block['difficulty'])
        my_hash = hashlib.sha256(digest.encode()).hexdigest()
        return True

    def hash(self, block):

        data = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha512(data).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

    def getLastTransaction(self):
        return self.transactions[-1]

    def length(self):
        return len(self.chain)

    def pop(self):
        self.chain.pop()
        if len(self.transactions) > 0:
            self.transactions.pop()

    def updateChain(self, chain):
        self.chain = chain
