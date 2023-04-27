from typing import Dict
import socket  # Import the socket library for network communication
import time  # Import the time library for time-related functions
import random  # Import the random library for generating random numbers and choices
import struct  # Import the struct library for working with packed binary data
import datetime

# Replace the following with the IP address of the machine running the server
SERVER_IP = "10.29.122.25"  # Define the server IP address (localhost in this case)
SERVER_PORT = 21200  # Define the server port number

# Path to save data
SAVE_PATH = "../../data"

def write_data(data_dict: Dict[str, float], verbose=True):
    now_utc_stamp = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

    for key, value in data_dict.items():
        if verbose:
            print(f"Received {key}:", key)

        with open(f'./ur5_{key}.csv', 'a') as f:
            f.write(f'{now_utc_stamp}, {value}\n')


def main():  # Define the main function
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Create a TCP socket
        s.connect((SERVER_IP, SERVER_PORT))  # Connect to the server
        print("Connected to server")  # Print a message indicating successful connection

        while True:  # Run an infinite loop
            message = random.choice(["UP", "DOWN", " "])  # Choose a random message from the list
            s.sendall(message.encode())  # Send the message to the server

            data = s.recv(1024)  # Receive data from the server (up to 1024 bytes)
            # FIXME: Need to recieve not only torque but also displacement
            torques = struct.unpack("!" + "f" * 6, data)  # Unpack the received packed binary data into a tuple of 6 floats
            data_dict = {
                f'torque{i}': t for i, t in enumerate(torques)
            }
            write_data(data_dict, verbose=True)

            time.sleep(1)  # Wait for 1 second before sending the next message


if __name__ == "__main__":
    main()  # Run the main function when the script is executed
