import socket
 
 
# Constants
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"
 
 
def start_server():
   # Create a socket object
   server_socket = socket.socket()
   # This Bind the socket to all IP addresses of this host
   server_socket.bind((SERVER_HOST, SERVER_PORT))
   # Make the port reusable
   server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   # Start listening for incoming connections
   server_socket.listen(5)
   print(f"[*] The Pycodes is Listening as {SERVER_HOST}:{SERVER_PORT}")
 
 
   # Accept connections
   client_socket, client_address = server_socket.accept()
   print(f"[+] {client_address[0]}:{client_address[1]} Connected to The Pycodes")
 
 
   # Receive the current working directory of the client
   cwd = client_socket.recv(BUFFER_SIZE).decode()
   print(f"[+] Current working directory: {cwd}")
 
 
   while True:
       # Get command from user
       command = input(f"{cwd} $> ")
       if not command.strip():
           continue
       # Send command to client
       print(f"[DEBUG] Sending command: {command}")
       client_socket.send(command.encode())
       if command.lower() == "exit":
           break
 
 
       # Receive and print command output
       output = client_socket.recv(BUFFER_SIZE).decode()
       results, cwd = output.split(SEPARATOR)
       print(f"[DEBUG] Received output: {results}")
       print(results)
 
 
   # Close sockets
   client_socket.close()
   server_socket.close()
 
 
if __name__ == "__main__":
   start_server()
