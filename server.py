import os
from threading import Thread
import socket

# a thread class to handle each client connection
class ClientHandler(Thread):
    def __init__(self, sock):
        super().__init__(daemon=True)
        self.sock = sock

    def run(self):
        # remove all trailing null pad bytes
        filename = self.sock.recv(1024).rstrip(b'\x00').decode()

        if filename:
            # checking whether names conflict and generating a new name if needed
            if os.path.isfile(filename):
                duplicate_counter = 1
                while True:
                    new_filename = filename + f'_copy_{duplicate_counter}'
                    if not os.path.isfile(new_filename):
                        filename = new_filename
                        break
                    else:
                        duplicate_counter += 1
            with open(filename, 'wb') as file:
                # fetching data from TCP connection and writing to output file
                while True: 
                    data = self.sock.recv(1024)
                    if data:
                        file.write(data)
                    else:
                        break
        self.sock.close()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8800))
sock.listen()

while True:
    connection, addr = sock.accept()
    # for each new connection deploy a thread to handle it
    ClientHandler(connection).start()

sock.close()