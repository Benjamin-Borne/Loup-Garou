import socket 
import threading

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(0)
	try:
            
		s.connect(('10.254.254.254', 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP

# Liste pour stocker les connexions clients
clients = []

# Fonction pour gérer un client
def handle_client(client_socket, address):
    print(f"[NOUVEAU CLIENT] {address} connecté.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[{address}] {message}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    print(f"[DÉCONNECTÉ] {address} a quitté.")
    clients.remove(client_socket)
    client_socket.close()

# Diffuser un message à tous les clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Configuration du serveur
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("IP_LOCAL", 12345))  # Écoute sur toutes les IP locales, port 12345
    server.listen(5)  # Jusqu'à 5 connexions en file d'attente
    print("[DÉMARRÉ] Serveur en attente de connexions...")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

# Lancer le serveur
if __name__ == "__main__":
    start_server()

