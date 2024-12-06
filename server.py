import socket
import threading
import base64

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
    
    
def keygen(chaine : str) -> str:
    return base64.b64encode(chaine.encode()).decode()
    
def keygenRev(key : str) -> str:
    return base64.b64decode(key.encode()).decode()


class ChatServer:
    def __init__(self, host="192.168.1.66", port=5000):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []
        self.pseudo = []
	
	
    def getClients(self):
    	return self.clients

    def getPseudo(self):
    	return self.pseudo


    def handle_client(self, client_socket, address):
        print(f"[NOUVEAU CLIENT] {address} connecté.")
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                
                if message:
                    if message.split("$")[0] == "pseudo":
                    	self.pseudo.append(message.split("$")[1]) if message.split("$")[1] not in self.pseudo else None
                    	print(self.pseudo)
                    self.broadcast(message, client_socket)
                else:
                    break
            except:
                break

        print(f"[DÉCONNECTÉ] {address} a quitté.")
        self.clients.remove(client_socket)
        client_socket.close()
    
    def send(self, message, destination):
    	destination.send(message)
    	    
    	    
    	    
    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()
                    self.clients.remove(client)

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"[DÉMARRÉ] Serveur en attente de connexions sur {self.host}:{self.port}...")

        while True:
            client_socket, client_address = self.server.accept()
            self.clients.append(client_socket)
            thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            thread.start()

