# Module 1 - Creating a blockchain! 
#here adding one moe libraray: requests=2.18.4 using pip install requests==2=18.4
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid         #THIS IS USED TO CREAETE ADDRESS OF NODES, IT GENERATE RANDOM ADDRESSES, WE JUST NEED TO REMOVE THE '-'IN THE ADDRESS 
from urllib.parse import urlparse

class BlockChain:
    def __init__(self):
        self.chain = []
        self.transactions=[]    #this postn is imp, ie b4 create block is called, as it will use this list
        self.create_block(proof=1,previous_hash='0')
        self.nodes=set()
    
    def create_block(self, proof, previous_hash):
        block= {'index':len(self.chain)+1,
                'timestamp':str(datetime.datetime.now()),
                'proof':proof,
                'transactions':self.transactions,       #added the txns here,postn does nt matter.
                'previous hash':previous_hash}
        self.transactions=[]        #after adding all the txns , make it a emoty list   
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation= hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof=True
            else:
                new_proof=new_proof+1
        return new_proof
            
    def hash(self, block):
        encoded_block=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
       prev_block=chain[0]
       block_index=1
       while block_index<len(chain):
           block=chain[block_index]
           if block['previous hash'] !=self.hash(prev_block):
               return False
           previous_proof=prev_block['proof']
           proof=block['proof']
           hash_operation= hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
           if hash_operation[:4]!='0000':
               return False
           prev_block=block
           block_index+=1
       return True
    def add_transaction(self,sender,receiver,amount):
        self.transactions.append({'sender':sender,'receiver':receiver,'amount':amount})
        previous_block=self.get_previous_block()
        return previous_block['index']+1
    
    def add_node(self, address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)       #.netloc se we get the url of the node, oly ip id, withoud http, basically what we wanted , a unique specifier
        
    def replace_chian(self):
        network=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        for node in network:
            response=requests.get(f'http://{node}get_chain')
            if response.status_code==200:
                length=response.json()['length']
                chain=response.json()['chain']
                if length>max_length and self.is_chain_valid(chain):
                    max_length=length
                    longest_chain=chain
        if longest_chain:
            self.chain=longest_chain
            return True
        else:
            return False
    #MINING our BLOCKCHIAN
    
   #1st creating a web app using flask 
       
app=Flask(__name__)


#Creating an address for the node on port 5000
node_address=str(uuid4().replace('-',''))

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
 #2 CReating our blockcahin on this web app
blockchain = BlockChain()
    #mining a new block 
@app.route('/mine_block', methods=['Get'])
def mine_block():
    prev_block=blockChain.get_previous_block()
    previous_proof=prev_block['proof']
    proof=blockChain.proof_of_work(previous_proof)
    prev_hash=blockChain().hash(prev_block)
    blockchain.add_transaction(sender=node_address, receiver="Samyak", amount=100)
    blockchain.add_transaction(sender=node_address, receiver="Sanjita", amount=50)
    blockchain.add_transaction(sender=node_address, receiver="Rupsss", amount=50)
    block=blockChain().create_block(proof, prev_hash)
    response= {'message':'Congo, you just mined a block!',
               'index':block['index'],
               'TimeStamp':block['timestamp'],
               'Previous Hash':block['previous hash']
               'Transactions:'block['transactions']}
    return jsonify(response), 200           #200 is http code for success of get  

@app.route('/get_chain', methods=['Get'])   

def get_chain():
    response={'chain':blockchain.chain,
              'Length':len(blockchain.chain),
              }
    return jsonify(response),200

  


@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200
#Adding  new transactions to the Blockchain
 
@app.route('/add_transaction', methods'= ['POST'])
def add_transaction():
    json=request.get_json()
    transaction_keys=['sender','receiver','amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements are missing :(',400
    index=blockchian.add_transaction(json['sender'],json['receiver'],json['amount'])
    response={'message':f'This transactions will be added to the Block {index}'}
    return jsonify(response),201
app.run(host='0.0.0.0', port=5000) 

#Decentralizing our Blockchain
#Connecting new nodes

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json=request.get_json()
    nodes=json.get('nodes')
     if nodes=None:
         return 'No node',400
     for node in nodes:
         blockchain.add_node(node)
     response={'message':'All the nodes are connected, and the Hadcoin blockchain now has the following nodes :',
               'total nodes':list(blockchain.nodes)}
     return response,201
 
#Replacing the chain by the longest chain if needed

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes have different chains, so the chain was replaced by the longesst one',
                    'now chain':blockchain.chain}
    else:
        response = {'message': 'All good, this chain is the longest chain.',
                    'Actual chain':blockchain.chain}
    return jsonify(response), 200

#Running the app
app.run(='0.0.0.0',port=5000)


