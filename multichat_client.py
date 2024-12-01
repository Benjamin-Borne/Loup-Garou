import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}")
        except:
            print("[ERREUR] Connexion au serveur perdue.")
            client_socket.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "IP_LOCAL du serveur"
    server_port = 12345

    try:
        client.connect((server_ip, server_port))
        print("[CONNECTÉ] Connexion au serveur réussie.")
    except:
        print("[ERREUR] Impossible de se connecter au serveur.")
        return

    username = input("Entrez votre nom d'utilisateur : ")
    client.send(f"{username} a rejoint le chat.".encode('utf-8'))

    # Thread pour recevoir des messages
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    # Envoyer des messages
    while True:
        message = input("aaa")
        if message.lower() == "quit":
            client.send(f"{username} a quitté le chat.".encode('utf-8'))
            client.close()
            break
        client.send(f"{username}: {message}".encode('utf-8'))

if __name__ == "__main__":
    start_client()

