import socket
import time
from threading import Thread

SERVER_HOST = "192.168.1.101"
SERVER_PORT = 5002
separator_token = "<SEP>"
counter = 0
tappost = True
client_sockets = set()
#client.socket = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
	while True:
		try:
			msg = cs.recv(1024).decode()
			#name_shared = cs.recv(1024).decode()
		except Exception as e:
			print(f"[!] Error: {e}")
			tappost = False
			client_sockets.remove(cs)
		else:
			msg = msg.replace(separator_token, ": ")

		#print("[Client]", msg)
		for client_socket in client_sockets:
			client_socket.send(msg.encode())
			print("[Client]", msg)

while True:
	client_socket, client_address = s.accept()
	"""messaggio = f"{client_address}\n"
	messaggio = client_address[0] + ":" + str(client_address[1])
	print(messaggio)
	client_socket.send(messaggio.encode())"""

	print(f"[+] {client_address} connected.")
	client_sockets.add(client_socket)
	#counter = counter  + 1
	#if counter == 1:
	
	t = Thread(target=listen_for_client, args=(client_socket,))
	t.daemon = True
	t.start()





for cs in client_sockets:
	cs.close()
s.close()
