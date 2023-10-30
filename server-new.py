#  server.py

import socket
import threading
import os

#  Server hostname or IP address
HOST = "127.0.0.1"

#  Port used by server
PORT = 65432

BUFFER_SIZE = 4096

#  Store connected clients
client_list = []


#  Handle client communication
def handle_client(client_socket):
    while True:
        #  Receive data (up to 1024 bytes at a time) from client
        data = client_socket.recv(1024).decode()
        if not data:
            break

        #  Handling file
        if data.startswith("FILE:"):
            #  Extract file name
            file_name = data[5:]
            # acknowledgment = "READY"
            # client_socket.send(acknowledgment.encode())
            print(f"File '{file_name}' received.")
            # send_file(client_socket, file_name)
            # print(f"File '{file_name}' received successfully.")
        else:
            print(f"Received from client: {data}")
            #  Prompt server for a message
            msg = input("[Server] Type message: ")
            #  Send server msg to client
            client_socket.send(msg.encode())


def send_file(server_socket, file_name):
    try:
        # Send the filename to the server
        server_socket.send(f"FILE:{file_name}".encode())
        print(f"File '{file_name}' sent.")

        # Receive acknowledgment from the server
        # acknowledgment = client_socket.recv(1024).decode()

        # if acknowledgment == "READY":
        with open(file_name, "rb") as file:
            file_data = file.read(BUFFER_SIZE)
            while file_data:
                server_socket.send(file_data)
                file_data = file.read(BUFFER_SIZE)
            print(f"File '{file_name}' sent successfully to client")
        # else:
        #    print("Server is not ready to receive the file.")

    except FileNotFoundError:
        print(f"File '{file_name}' not found on the client.")
        server_socket.send(b"File not found on the client.")
    except Exception as e:
        print(f"Error sending file: {str(e)}")


#  create socket object
#  AF_INET: Internet address family for IPv4
#  SOCK_STREAM: socket type for TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    #  associates socket 'server' with specific local address (HOST) and port (PORT)
    #  values depend on the address family of socket
    #  HOST: standard IPv4 address for loopback interface
    #  PORT: TCP port number to accept connections from clients
    server.bind((HOST, PORT))
    #  listen does have OPTIONAL backlog parameter
    #     specifies # of unaccepted connections that system will allow before refusing new ones
    #  enables the server to accept connection
    server.listen()
    print(f"Listening on {HOST}:{PORT}")
    #msg = input("[Server] Type message or 'FILE:<filename>' to send a file: ")

    while True:
        #  Accept incoming connection
        #  Obtain client socket and address
        #  accept: blocks execution and waits for incoming connection
        #  returns a new socket object - the connection AND a tuple holding address of client (host, port)
        conn, addr = server.accept()
        print(f"{addr} is connected")

        #  Add client socket to list of connected clients
        client_list.append(conn)

        #  Create separate thread to handle communication with the client
        #  conn socket is passed in as parameter when client_handle thread is created
        #  handle_client when executed within thread, operates on specific client_socket
        #    to send and receive data to and from connected client
        client_handler = threading.Thread(target=handle_client, args=(conn,))
        client_handler.start()

