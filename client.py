import socket

host = '192.168.197.63'
port = 5000

serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur_socket.connect((host, port))

print(f"connecté à {port}")

serveur_socket.send("EOF".encode('utf-8'))

print("close")
serveur_socket.close()

