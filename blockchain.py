import json
import os
import hashlib
import time

CHAIN_FILE = 'chain.json'

class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def create_block(self, sender, receiver, message, previous_hash=''):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'previous_hash': previous_hash,
            'hash': ''
        }
        block['hash'] = self.hash(block)
        return block

    def add_block(self, sender, receiver, message):
        previous_hash = self.chain[-1]['hash'] if self.chain else '0'
        block = self.create_block(sender, receiver, message, previous_hash)
        self.chain.append(block)
        self.save_chain()

    def hash(self, block):
        block_copy = block.copy()
        block_copy['hash'] = ''
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as file:
            json.dump(self.chain, file, indent=4)

    def load_chain(self):
        if os.path.exists(CHAIN_FILE) and os.path.getsize(CHAIN_FILE) > 0:
            with open(CHAIN_FILE, 'r') as file:
                self.chain = json.load(file)
        else:
            self.chain = []
