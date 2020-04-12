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
from flask import flask, jsonify

#parte 1, criar um blockchain

class Blockchain:
    def __init__(self):
        self.chain = [] #inicializando uma lista
        self.create_block(proof = 1, previuos_hash = '0')
        
    def create_block(self, proof, previous_hash):
        #criando um dicionario
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        self.chain.append(block) #adicionar um elemento na Lista
        return block
    
    
    #criar um metodo para retornar o block anterior
    
    def get_previous_block(self):
        return self.chain[self.chain - 1]
    
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

































