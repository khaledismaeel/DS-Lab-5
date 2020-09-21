import sys
import os
import socket
import tqdm

filename = sys.argv[1]
ip_address = sys.argv[2]
port_number  = sys.argv[3]

# opening the necessary file and socket
file = open(filename, 'rb')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip_address, int(port_number)))

# encoding and padding filename
sent_filename = filename.encode()
while len(sent_filename) < 1024:
    sent_filename += b'\0'

# sending filename
sock.send(sent_filename)

progress_bar = tqdm.tqdm(range(os.path.getsize(filename)), unit = 'B', unit_scale = True, unit_divisor = 1024)

# sending the actual file
while True: 
    data = file.read(1024)
    if data:
        sock.send(data)
        progress_bar.update(len(data))
    else:
        break

sock.close()
file.close()