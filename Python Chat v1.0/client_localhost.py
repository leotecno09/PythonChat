import socket
import random
from threading import *
import threading
from datetime import datetime
from colorama import Fore, init, Back

init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]
error_prefix = "[Errore]"
tappost = True

client_color = random.choice(colors)

SERVER_HOST = "192.168.1.101"
SERVER_PORT = 5002
separator_token = "<SEP>"

name = input("Inserisci il tuo nickname: ")
#name_shared = name
#msg_identificazione = f"xxx:{name}\n"
s = socket.socket()
print (f"[*] Connessione a {SERVER_HOST}:{SERVER_PORT}...")
try:
    s.connect((SERVER_HOST, SERVER_PORT))
except ConnectionRefusedError:
    print (error_prefix, "Connessione rifiutata dal Server. (ConnectionRefusedError)")
    tappost = False
except TimeoutError:
    print (error_prefix, "Impossibile localizzare il Server. (TimeoutError)")
    tappost = False
#s.send(msg_identificazione.encode())
if tappost == True:
    print ("[+] Connesso")
if tappost == False:
    print("\n[-] Connessione terminata.")
    quit()
#message = s.recv(1024).decode()
#print("\n" + message)


def listen_for_messages():
    try:
        while True:

        #print("ciao\n")
            message = s.recv(1024).decode()
            #name_shared = s.recv(1024).decode()
            print("\n" + message)
    except ConnectionResetError:
        print(error_prefix, "Connessione interrotta dal Server. (ConnectionResetError)")
        tappost = False
    except ConnectionAbortedError:
        print("[-] Connessione Terminata.")


listen_thread = threading.Thread(target=listen_for_messages)
#listen_thread.daemon = True
listen_thread.start()

while True:
    to_send = input()

    if to_send.lower() == "q":
        break

    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    to_send = f"<{name}> {to_send}\n"

    s.send(to_send.encode())

s.close()
