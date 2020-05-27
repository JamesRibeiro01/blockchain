import json
from firebase import firebase

firebase = firebase.FirebaseApplication('https://projetotcc-89335.firebaseio.com/', None)
responseRequest = firebase.get('/contatos/', '')
print(responseRequest)
for alunoID in responseRequest:

    arrayData = responseRequest[alunoID]

    print('Nome do aluno: ' + arrayData['nomeAluno'])


