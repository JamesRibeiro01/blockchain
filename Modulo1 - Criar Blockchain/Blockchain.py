# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 18:32:44 2020

@author: thiago
"""

"""
Importar a liby dateTime 
pq cada bloco quando for criado vai ter sua data exata

Importar a liby hashlib
pq vai ser produzido hashs

import json
vai codificar os blocos com json antes e depois gerar os hashs

from flask import flask, jsonify -> para produzir arquivos em formato json
"""

#Parte 1 -> criar um blockchain
#criar uma classe blockchain
#classe começa com a function init -> self quer dizer que as variaveis da classe se referem a propria classe
#Vamos ter uma propriedade que vai ser uma lista que vai conter o block
#inicializando uma lista em python
#implementando a função create block
#criando um dicionario, indicce, time stamp, elemnto proof, e o previous
import datetime
import hashlib
import json
from flask import Flask, jsonify
from firebase import firebase

firebase = firebase.FirebaseApplication('https://projetotcc-89335.firebaseio.com/', None)
responseRequest = firebase.get('/contatos/', '')
#print(result)

#parte 1, criar um blockchain


class Blockchain:
    def __init__(self):
        self.chain = [] #inicializando uma lista
        self.create_block(proof =1, previous_hash ='0')
        
        
    def create_block(self, proof, previous_hash):
        studentData = []
        #criando um dicionario
        for studentID in responseRequest:
            studentData = responseRequest[studentID]
            
        block = {'index': len(self.chain) + 1,
                     'timestamp': str(datetime.datetime.now()),
                     'proof': proof,
                     'previous_hash': previous_hash,
                     'Student_Name': studentData['nomeAluno'],
                     'Course': studentData['curso'] ,
                     'Email': studentData['email'],
                     'Registration': studentData['matricula'],
                     'Password': studentData['senha']}
        
        self.chain.append(block) #adicionar um elemento na Lista
        return block
    
    
    #criar um metodo para retornar o block anterior
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            
            else:
                new_proof += 1
        return new_proof
            
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True








#instanciar a class blockchain e inicializar a aplicação web com flask
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET']) # pagina para mineração do blockchain

#criar a função de mineração

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)    
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Parabens você minerou um bloco!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'Student_Name': block['Student_Name'],
                'Course': block['Course'] ,
                'Email': block['Email'],
                'Registration': block['Registration'],
                'Password': block['Password']
                }
    
    return jsonify(response), 200


@app.route('/get_chain', methods = ['GET']) #pargina para verificar todo o blockchain

def get_chain():
    response = {
                'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }
    return jsonify(response), 200


app.run(host = '0.0.0.0', port = 5000)















