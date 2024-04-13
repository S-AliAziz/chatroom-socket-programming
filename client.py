import socket
import threading

while True:
    userOption = input("Enter number 1 to register and enter number 2 to enter your account: ")

    if userOption == "1":
        while True:
            userName = str(input("Please choose a user name for your account: "))
            if ' ' in userName:
                print("ERROR : Username cannot have space. \n")
                continue
            else: 
                break
        while True:
            password = str(input("Please choose a password for your account: "))
            if ' ' in password:
                print("ERROR : Password cannot have space. \n")
                continue
            else: 
                break
        userDecision = f'Registration {userName} {password}'
        break
    elif userOption == "2":
        userName = input("Enter your user name: ")
        password = input("Enter your password: ")
        userDecision = f'Login {userName}'
        break
    else:
        print("ERROR: The input is not valid. Please choose option 1 or 2. \n")
        continue




    


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 15000))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'OK' :
                client.send(userDecision.encode('ascii'))

            elif message == 'SEND_NAME&PASS':
                client.send(f'{userName} {password}'.encode('ascii'))

            elif message == 'SEND_NICK':
                client.send(nickname.encode('ascii'))

            elif message =='ERROR':
                print('Sign up failed. Your choosen username has already taken. Please try again')
                client.close()
                break

            else:
                print(message)
            
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{userName}: {input("")}'
        client.send(message.encode('ascii'))
                
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()