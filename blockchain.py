# Module 1 - Creating a blockchain! 
import datetime
import hashlib
import json
from flask import Flask, jsonify

class BlockChain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1,previous_hash='0')
    
    def create_block(self, proof, previous_hash):
        block= {'index':len(self.chain)+1,
                'timestamp':str(datetime.datetime.now()),
                'proof':proof,
                'previous hash':previous_hash}
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
   
    
   #MINING our BLOCKCHIAN
    
   #1st creating a web app using flask 
       
app=Flask(__name__)
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
    block=blockChain().create_block(proof, prev_hash)
    response= {'message':'Congo, you just mined a block!',
               'index':block['index'],
               'TimeStamp':block['timestamp'],
               'Previous Hash':block['previous hash']}
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


#running the app 
app.run(host='0.0.0.0', port=5000) 










