import socket

class Connection:
    def __init__(self):
        self.sock = None

    def connect(self, ip, port):
        print(f"Tentativo di connessione a IP: {ip}, Porta: {port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((ip, int(port)))  # Assicurati che la porta sia un intero
            return 'online'
        except socket.gaierror as e:
            print(f"Errore di risoluzione dell'indirizzo: {e}")
            return 'offline'
        except ConnectionRefusedError as e:
            print(f"Connessione rifiutata: {e}")
            return 'offline'
        except socket.timeout as e:
            print(f"Timeout della connessione: {e}")
            return 'offline'
        except socket.error as e:
            print(f"Altro errore di connessione: {e}")
            return 'offline'

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def send(self, message):
        if self.sock:
            self.sock.sendall(message.encode())

    def receive(self):
        if self.sock:
            return self.sock.recv(1024).decode()
