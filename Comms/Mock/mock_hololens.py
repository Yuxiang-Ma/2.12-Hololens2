import socket  # Import the socket library for network communication
import time  # Import the time library for time-related functions
import random  # Import the random library for generating random numbers and choices
import struct  # Import the struct library for working with packed binary data

# Replace the following with the IP address of the machine running the server
server_ip = "10.29.122.25"  # Define the server IP address (localhost in this case)
server_port = 21200  # Define the server port number

def main():  # Define the main function
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Create a TCP socket
        s.connect((server_ip, server_port))  # Connect to the server
        print("Connected to server")  # Print a message indicating successful connection

        while True:  # Run an infinite loop
            message = random.choice(["UP", "DOWN", " "])  # Choose a random message from the list
            s.sendall(message.encode())  # Send the message to the server

            data = s.recv(1024)  # Receive data from the server (up to 1024 bytes)
            torques = struct.unpack("!" + "f" * 6, data)  # Unpack the received packed binary data into a tuple of 6 floats
            print("Received torques:", torques)  # Print the received torques

            time.sleep(1)  # Wait for 1 second before sending the next message

if __name__ == "__main__":
    main()  # Run the main function when the script is executed
