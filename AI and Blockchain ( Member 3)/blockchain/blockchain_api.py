from flask import Flask, jsonify, request
from blockchain import Blockchain # Import our Blockchain class

# Instantiate the Node
app = Flask(__name__)

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/get_chain', methods=['GET'])
def get_chain():
    """Returns the full blockchain."""
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """Receives transaction data and adds it to the blockchain."""
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['donor_id', 'hospital_id', 'blood_type', 'status']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction and "mine" a new block
    index = blockchain.new_transaction(values['donor_id'], values['hospital_id'], values['blood_type'], values['status'])
    
    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof=12345, previous_hash=previous_hash) # Using a placeholder proof

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) # Running on a different port (5001)