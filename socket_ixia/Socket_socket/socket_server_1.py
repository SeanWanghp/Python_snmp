




import socket                   # Import socket module

port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print('Server listening....')

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    data = conn.recv(1024)
    print('Server received', repr(data))

    filename = 'socket_server_1.txt'
    f = open(filename, 'rb')
    in_data = f.read(1024)
    while (in_data):
       conn.send(in_data)
       print('Sent ', repr(in_data))
       in_data = f.read(1024)
    f.close()

    print('Done sending')
    conn.send('\n. Thank you for connecting')
    conn.close()
