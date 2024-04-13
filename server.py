import threading
import socket

# from crypto.Random import get_random_bytes
# from crypto.Protocol.KDF import PBKDF2
# from crypto.Cipher import AES
# from crypto.Util.Padding import pad, unpad
# import base64


host = 'localhost'
port = 15000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

class User:
    def __init__(self, userName, password, client, address, isOnline=True):
        self.userName = userName
        self.password = password
        self.isOnline = isOnline
        self.client   = client
        self.address  = address

users = []
userNames = []

ali = User("aliaziz",1234,'','')

def encrypt(orginalText, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_orginalText = pad(orginalText.encode('ascii'), AES.block_size)
    cipherText = cipher.encrypt(padded_orginalText)
    return base64.b64encode(iv + cipherText).decode('ascii')

def decrypt(cipherText, key):
    cipherText = base64.b64decode(cipherText)
    iv = cipherText[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded_orginalText = cipher.decrypt(cipherText[AES.block_size:])
    orginalText = unpad(decrypted_padded_orginalText, AES.block_size)
    return orginalText.decode('ascii')

def errorHandling(client):
    client.send('ERROR'.encode('ascii'))
    client.close()

def getUser(userName):
    for user in users:
        if userName == user.username:
            return user
    return False

def logOut(user):
    users[user].isOnline = False
    users[user].client = ''
    users[user].address = ''

def signUp(userName, password,client,address):
    for user in users:
        userNames.append(user.userName)
    if userName in userNames:
        print("ERROR: There is an account with this user name.")
        client.send('ERROR'.encode('ascii'))
        # client.close()

        # users.append(User('userName', password, client,address))

        # client.close()
    else:
        print("line 34")
        users.append(User(userName, password, client,address))


# def logIn(userName, password):


def broadcast(message):
    for user in users:
        if user.isOnline == True:
            user.client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            for user in users:
                if user.client == client :
                    userName = user.userName
                    logOut(users.index(user))
            broadcast(f'{userName} left the chat:'.encode('ascii'))
            client.close()
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('OK'.encode('ascii'))
        userDecision = client.recv(1024).decode('ascii')


        if userDecision.startswith("Registration"):
            userInfo = userDecision.split(' ')
            userName = userInfo[1]
            password = userInfo[2]   
            signUp(userName, password, client, address)
            
        elif userDecision.startswith("Login"):
            userInfo = userDecision.split(' ')
            userName = userInfo[1]
            # currentUser = getUser(userName)
            # if currentUser is False :
            #     errorHandling(client)
            #     continue

            # # signUp(userName, 1234, client, address)
            # salt = get_random_bytes(32)
            # key = PBKDF2(password=currentUser.password, salt=salt, dkLen=32)
            # client.send(b'Key ' + salt )
            # logIn(userName)

        # userOption = client.recv(1024).decode('ascii')

        # if userOption == "SIGN_UP":
        #     client.send('SEND_NAME&PASS'.encode('ascii'))
        #     info = client.recv(1024).decode('ascii').split(' ')
        #     userName = info[0]
        #     password = info[1]
        #     signUp(userName, password, client, address)

        # elif userOption == "LOG_IN":
        #     client.send('SEND_NICK'.encode('ascii'))
        #     userName = client.recv(1024).decode('ascii')
        signUp(userName, 1234, client, address)


        print(f'Nickname of the client is {userName}!')
        broadcast(f'{userName} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()