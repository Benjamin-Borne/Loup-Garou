import socket
import server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_serv = "192.168.0.13"
port = 5000

client.connect((ip_serv, port))
print("Connecté batard")

