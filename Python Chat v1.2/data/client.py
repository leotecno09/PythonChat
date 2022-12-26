import socket
import random
from threading import *
import threading
from datetime import datetime
from colorama import Fore, init, Back
import os
import subprocess
from pyngrok import ngrok

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(0)



init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]
error_prefix = "[Error]"
tappost = True


client_color = random.choice(colors)

separator_token = "<SEP>"

print ("Welcome to Pychat 1.2!")
print ("***************************")
print ("Select one of this options to start:")
print ("1) Start a private chat\n2) Start a public chat (using Ngrok)\n3) Connect to an existing chat")
option = int(input(""))

if option == 1:
    os.startfile('.\data\server_localhost.py')
    print ("Chat generated - server started!")
    print ("[+] Connecting you automatically to the chat generated.")
    SERVER_HOST = "localhost"
    SERVER_PORT = 5002
if option == 2:
    print ("For this option you need to know what is Ngrok and how it works and create an account to https://ngrok.com and next you have to copy your AUTHTOKEN from https://dashboard.ngrok.com/get-started/your-authtoken")
    ngrokauthfile = open("./data/ngrok_user_authtoken.txt", "r")
    size = os.path.getsize('./data/ngrok_user_authtoken.txt')
    if size == 0:
        authtokenuser = str(input("Insert your authtoken here: "))
        ngrokauthfile = open("./data/ngrok_user_authtoken.txt", "w")
        ngrokauthfile.write(authtokenuser)
        ngrok.set_auth_token(authtokenuser)
    else:
        with open("./data/ngrok_user_authtoken.txt") as atfile:
            authcontent = atfile.read()
            #print (authcontent)
            print ("Automatically set Ngrok authtoken")
            ngrok.set_auth_token(authcontent)


    print ("Done! Generating the chat.")
    os.startfile('.\data\server_localhost.py')
    print ("[+] Chat generated - server started!")
    ngroktunnel = ngrok.connect(5002, "tcp")
    #tunnels = ngrok.get_tunnels()
    print ("Here's your", ngroktunnel)
    SERVER_HOST = "localhost"
    SERVER_PORT = 5002
    print ("[+] Connecting you automatically to the chat generated.")
if option == 3:
    ip = str(input("Insert the chat IP: "))
    port = int(input("Insert the chat port (if not specified put 5002): "))
    SERVER_HOST = ip
    SERVER_PORT = port

name = input("Insert your nickname: ")
name_shared = name
#msg_identificazione = f"xxx:{name}\n"

s = socket.socket()
print (f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
try:
    s.connect((SERVER_HOST, SERVER_PORT))
except ConnectionRefusedError:
    print (error_prefix, "Connection refused by Server. (ConnectionRefusedError)")
    tappost = False
except TimeoutError:
    print (error_prefix, "Unable to locate Server. (TimeoutError)")
    tappost = False
#s.send(msg_identificazione.encode())
if tappost == True:
    print ("[+] Connected.")
if tappost == False:
    print("\n[-] Connection terminated.")
    print ("\nThe reconnect function is not implemented, please reconnect manually.")
    os.system("pause")
    quit()
#message = s.recv(1024).decode()
#print("\n" + message)


def listen_for_messages():
    try:
        while True:

        #print("ciao\n")
            message = s.recv(1024).decode()
            #name_shared = s.recv(1024).decode()
            print("\n" + client_color + message)
    except ConnectionResetError:
        print(error_prefix, "Connection closed by Server. (ConnectionResetError)")
        tappost = False
    except ConnectionAbortedError:
        print("[-] Connection terminated.")

listen_thread = threading.Thread(target=listen_for_messages)
#listen_thread.daemon = True
listen_thread.start()

while True:
    to_send = input()

    if to_send.lower() == "q":
        print ("Closing!")
        s.close()
        exit()

    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    to_send = f"<{name}> {to_send}\n"

    s.send(to_send.encode())


s.close()
