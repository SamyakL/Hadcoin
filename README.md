#**Hadcoin**

Hadcoin is a simple cryptocurrency implemented in Python, designed to simulate the fundamental aspects of blockchain technology, including mining, transaction handling, and network communication. This project serves as an educational tool to understand the basics of cryptocurrencies and blockchain mechanics.

##Features

###Blockchain Structure: Implements a chain of blocks, each containing a list of transactions, a proof (nonce), and the hash of the previous block.
###Proof-of-Work Mechanism: Utilizes a proof-of-work algorithm to secure the network and validate new blocks.
###Transaction Management: Allows the creation and handling of transactions between nodes.
###Node Network: Supports the addition of multiple nodes to form a decentralized network, enabling consensus across the blockchain.

###Project Structure
The project consists of the following Python scripts:
blockchain.py: Contains the core Blockchain class, which manages the chain, handles proof-of-work, and validates the blockchain.
hadcoin.py: Implements the Flask web application to interact with the blockchain via HTTP requests.

##Installation
Ensure you have Python installed. It's recommended to use a virtual environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```
Install the required packages:
```
pip install Flask==2.0.1
```

###Usage

Starting the Node:
Run the Flask application to start a node:
```
python hadcoin.py
```
By default, the node will run on http://127.0.0.1:5000/


Mining a New Block:
To mine a new block, send a GET request to /mine_block:
```
curl http://127.0.0.1:5000/mine_block
```
This will execute the proof-of-work algorithm, create a new block, and add it to the blockchain.


Viewing the Blockchain:
To retrieve the current state of the blockchain, send a GET request to /get_chain:
```
curl http://127.0.0.1:5000/get_chain
```

Adding a Transaction:
To add a new transaction, send a POST request to /add_transaction with a JSON payload containing the sender, receiver, and amount:
```
curl -X POST -H "Content-Type: application/json" -d '{
  "sender": "address1",
  "receiver": "address2",
  "amount": 10
}' http://127.0.0.1:5000/add_transaction
```
The transaction will be added to the next mined block.

Connecting Nodes:
To connect multiple nodes and form a network, send a POST request to /connect_node with a JSON payload containing the list of node addresses:
```
curl -X POST -H "Content-Type: application/json" -d '{
  "nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]
}' http://127.0.0.1:5000/connect_node
```
This will enable the nodes to communicate and achieve consensus.


Replacing the Chain:
To ensure the node has the longest valid chain, send a GET request to /replace_chain
```
curl http://127.0.0.1:5000/replace_chain
```
If the current node's chain is shorter than any connected node's chain, it will be replaced with the longest one.

**License**
This project is licensed under the BSD-3-Clause License. See the LICENSE file for details
*Note: This project is for educational purposes and is not intended for production use.*
