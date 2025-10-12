import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Create the genesis block (the very first block in the chain)
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new Block and adds it to the chain.
        Each block contains the transactions added since the last block.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof, # A number to verify the block (placeholder for now)
            'previous_hash': previous_hash or self.hash(self.last_block),
        }
        
        # Reset the current list of transactions now that they're in a block
        self.current_transactions = []
        
        self.chain.append(block)
        return block

    def new_transaction(self, donor_id, hospital_id, blood_type, status):
        """
        Adds a new transaction to the list of transactions waiting to be mined.
        """
        self.current_transactions.append({
            'donor_id': donor_id,
            'hospital_id': hospital_id,
            'blood_type': blood_type,
            'status': status,
            'timestamp': time(),
        })
        # Return the index of the block that this transaction will be added to
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a secure SHA-256 hash of a block.
        """
        # We must make sure that the dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last block in the chain
        return self.chain[-1]
    # ADD THIS METHOD TO YOUR BLOCKCHAIN CLASS
    def is_chain_valid(self, chain):
        """
        Determine if a given blockchain is valid.
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            last_block = block
            current_index += 1
        
        return True

# --- Main execution block for testing ---
if __name__ == "__main__":
    # Instantiate the Blockchain
    bloodchain = Blockchain()
    print("✅ Blockchain created.")
    print("Genesis Block:", json.dumps(bloodchain.chain[0], indent=2))
    
    # Add a new transaction representing a blood donation
    print("\nAdding a 'Donated' transaction...")
    bloodchain.new_transaction(
        donor_id="DONOR_ANON_12345",
        hospital_id="BENGALURU_HOSPITAL_01",
        blood_type="O+",
        status="Donated"
    )
    
    # "Mine" a new block to add the transaction to the chain
    # In a real blockchain, 'proof' would be found by a complex algorithm. Here we just use a placeholder.
    last_block = bloodchain.last_block
    previous_hash = bloodchain.hash(last_block)
    new_block_proof = 12345 # Placeholder proof
    
    block = bloodchain.new_block(new_block_proof, previous_hash)
    
    print("\n✅ New block forged and added to the chain.")
    print("\n--- Current Blockchain ---")
    print(json.dumps(bloodchain.chain, indent=2, sort_keys=True))