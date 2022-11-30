import socket
import time
from threading import Thread
from datetime import datetime
from datetime import date
import sys
import win32api


SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
separator_token = "<SEP>"
counter = 0
tappost = True
client_sockets = set()
#client.socket = set()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
x = date.today()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
log = open("latest.log", "w")
log.write("[INFO] Recompiled the log on: "+ str(x) + "\n")
log.write("[INFO] Now listening.\n")
log.write("[INFO] Please note that the seconds writed in the log are not accurated! (We're working on it!)\n")
log.close()
print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
	while True:
		try:
			msg = cs.recv(1024).decode()
			#name_shared = cs.recv(1024).decode()
		except Exception as e:
			print(f"[!] Error: {e}")
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			log = open("latest.log", "a")
			log.write(current_time + f" There was an error {e}" + "\n")
			log.close()
			tappost = False
			client_sockets.remove(cs)
		else:
			msg = msg.replace(separator_token, ": ")

		#print("[Client]", msg)
		for client_socket in client_sockets:
			client_socket.send(msg.encode())
			print("[Client]", msg)
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			log = open("latest.log", "a")
			log.write(current_time + f" {client_address} " + msg + "\n")
			#time.sleep(2)
			log.close()

def on_exit(signal_type):
	exiting = str(input("Are you sure to close the server? (y/n) "))
	if exiting == "y" or exiting == "Y":
		print ("Closing the server!")
		log = open("latest.log", "a")
		log.write(current_time + " Server closed!\n")
		log.close()
		time.sleep(2)
		s.close()
		time.sleep(2)
		exit()
	else:
		print("Continue to work!")
		return(listen_for_client)

win32api.SetConsoleCtrlHandler(on_exit, True)


while True:
	client_socket, client_address = s.accept()
	"""messaggio = f"{client_address}\n"
	messaggio = client_address[0] + ":" + str(client_address[1])
	print(messaggio)
	client_socket.send(messaggio.encode())"""

	print(f"[+] {client_address} connected.")
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	log = open("latest.log", "a")
	log.write(current_time + f" {client_address} connected to the server.\n")
	log.close()
	client_sockets.add(client_socket)
	#counter = counter  + 1
	#if counter == 1:

	t = Thread(target=listen_for_client, args=(client_socket,))
	t.daemon = True
	t.start()






for cs in client_sockets:
	cs.close()
s.close()
