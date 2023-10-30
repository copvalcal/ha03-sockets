#  client.py

import socket
import os

#  Server hostname or IP address
HOST = "127.0.0.1"

#  Port used by server
PORT = 65432

#  Buffer size for data transmission
#  Send 4096 bytes each time step
BUFFER_SIZE = 4096

#  files for the transfer
file_1 = "data.csv"
file_2 = "test.txt"

#  getting file size
file_size_1 = os.path.getsize(file_1)
file_size_2 = os.path.getsize(file_2)


def send_file(client_socket, file_name):
    try:
        # Send the filename to the server
        client_socket.send(f"FILE:{file_name}".encode())
        print(f"File '{file_name}' sent.")

        # Receive acknowledgment from the server
        # acknowledgment = client_socket.recv(1024).decode()

        # if acknowledgment == "READY":
        with open(file_name, "rb") as file:
            file_data = file.read(BUFFER_SIZE)
            while file_data:
                client_socket.send(file_data)
                file_data = file.read(BUFFER_SIZE)
            print(f"File '{file_name}' sent successfully to server")
        # else:
        #    print("Server is not ready to receive the file.")

    except FileNotFoundError:
        print(f"File '{file_name}' not found on the client.")
        client_socket.send(b"File not found on the client.")
    except Exception as e:
        print(f"Error sending file: {str(e)}")


#  Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    #  Connect to the server
    print(f"[*] Connecting to {HOST}:{PORT}\n")
    client.connect((HOST, PORT))
    print("[*] Connected\n")

    #  Continuously send messages
    while True:
        # Get user input for msg
        msg = input("[Client] Type message or 'FILE:<filename>' to send a file: ")

        # Check if 'quit' sent
        if msg.lower() == 'quit':
            client.send(msg.encode())
            break

        if msg.startswith("FILE:"):
            file_name = msg[5:]
            client.send(msg.encode())
            send_file(client, file_name)
        else:
            # Send the encoded message to the server
            client.send(msg.encode())
            # Receive a response from the server
            data = client.recv(1024)
            print(f"Received from server: {data.decode()}")
            if msg.startswith("FILE:"):
                file_name = msg[5:]

