import socket, hashlib, os, time, rsa, sys, base64
from cryptography.fernet import Fernet


def initSetup():
	if not os.path.exists('keylist.perm'):
		check = ''
		check = input("\n\nIt appears this is your first time running the LightNet server. Would you like to conduct setup?: ")
		if check == ("y" or "Y" or "yes" or "YES"):
			createKeys()
				
			passw = Fernet.generate_key()
			print("\nThis is your Secure password, do not lose it: " + passw.decode())
			
			print("\n======================================================================================================\n")

			encryptKeys(passw)
			print("\nRSA keys have been generated and protected. Starting main module now!\n")
			
			print("======================================================================================================\n")
		else:
			exit()

		checkPass(False)
		createPass(adminPass)
		encryptPass(passw)



def initCheck():
	global public, private, passwordAdmin, passwordSecure
	passwordSecure = input("\n\nPlease input your Secure password: ")
	
	decryptKeys(passwordSecure)
	readKeys()
	public, private = readKey.split(b'|||||', 1)
	
	print("\nThank you!\n")
	
	if not os.path.exists('hashword.perm'):
		passwordAdmin = input("Please input an Admin password for this session: ")

	else:
		passwordAdmin = input("Please input your Admin password: ")
		decryptPass(passwordSecure)
		readPass()
		confirmPass(passwordAdmin, readPass)
	
	return public, private, passwordAdmin, passwordSecure
	
	

def hash(string):
	return hashlib.sha512(
		string
	).digest()
	
def hashString(str):
	return hashlib.sha512(
		str.encode()
	).digest()


def createKeys():
	publicKey, privateKey = rsa.newkeys(512)
	f = open('keylist.perm', 'wb')
	
	f.write(publicKey.save_pkcs1('PEM') + b'|||||' + privateKey.save_pkcs1('PEM'))
	f.close()
	
def encryptKeys(password):
	f = Fernet(password)
	with open('keylist.perm', 'rb') as original_file:
		original = original_file.read()
	encrypted = f.encrypt(original)
	original_file.close()
	with open ('keylist.perm', 'wb') as encrypted_file:
		encrypted_file.write(encrypted)
	encrypted_file.close()
	
def decryptKeys(password):
	f = Fernet(password)
	with open('keylist.perm', 'rb') as original_file:
		original = original_file.read()
	decrypted = f.decrypt(original)
	original_file.close()
	with open ('keylist.temp', 'wb') as decrypted_file:
		decrypted_file.write(decrypted)
	decrypted_file.close()
	
def readKeys():
	global readKey
	with open('keylist.temp', 'rb') as original_file:
		readKey = original_file.read()
	original_file.close()
	with open ('keylist.temp', 'wb') as decrypted_file:
		decrypted_file.write(b"1")
	decrypted_file.close()
	return readKey
	
	
	
def createPass(password):
	f = open('hashword.perm', 'w')
	f.write(str(hashString(password)))
	f.close()

def encryptPass(password):
	f = Fernet(password)
	with open('hashword.perm', 'rb') as original_file:
		original = original_file.read()
	encrypted = f.encrypt(original)
	original_file.close()
	with open ('hashword.perm', 'wb') as encrypted_file:
		encrypted_file.write(encrypted)
	encrypted_file.close()

def decryptPass(password):
	f = Fernet(password)
	with open('hashword.perm', 'rb') as original_file:
		original = original_file.read()
	decrypted = f.decrypt(original)
	original_file.close()
	with open ('hashword.temp', 'wb') as decrypted_file:
		decrypted_file.write(decrypted)
	decrypted_file.close()

def readPass():
	global readPass
	with open('hashword.temp', 'rb') as original_file:
		readPass = original_file.read()
	original_file.close()
	with open ('hashword.temp', 'wb') as decrypted_file:
		decrypted_file.write(b"1")
	decrypted_file.close()
	return readPass

def confirmPass(password, readPass):
	if str(hash(password.encode())) == readPass.decode():
		pass
	else:
		print("Invalid Admin password")
		exit()
		
def checkPass(big):
	global adminPass
	adminPass = input("\nPlease choose an Admin password: ")
	passw1 = input("\nPlease input your Admin password again: ")
	if adminPass != passw1:
		print("Passwords do not match!")
		return checkPass(False)
	l, u, p, d = 0, 0, 0, 0
	
	if big:
		if (len(adminPass) == 16):
			for i in adminPass:
				# counting lowercase alphabets 
				if (i.islower()):
					l+=1            
				# counting uppercase alphabets
				if (i.isupper()):
					u+=1            
				# counting digits
				if (i.isdigit()):
					d+=1            
				# counting the mentioned special characters
				if(i=='@'or i=='$' or i=='_'):
					p+=1           
			if not (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(adminPass)):
				print("Invalid Password. Requires uppercase, lowercase, number, special character, and must be 16 characters.")
				exit()
	else:
		if (len(adminPass) < 8):
			for i in adminPass:
				# counting lowercase alphabets 
				if (i.islower()):
					l+=1            
				# counting uppercase alphabets
				if (i.isupper()):
					u+=1            
				# counting digits
				if (i.isdigit()):
					d+=1            
				# counting the mentioned special characters
				if(i=='@'or i=='$' or i=='_'):
					p+=1           
			if not (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(adminPass)):
				print("Invalid Password. Requires uppercase, lowercase, number, special character, and must be at least 8 characters.")	
				exit()
	return adminPass
