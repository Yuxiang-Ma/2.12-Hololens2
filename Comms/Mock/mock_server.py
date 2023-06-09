"""
Example relay script for a UR5 robot and a HoloLens device.

Author: Chengyuan Ma

This script creates a communication bridge between a Universal Robots UR5 robotic arm and a HoloLens device. 
It allows the HoloLens to send control commands to the UR5 and receive real-time feedback of the robot's joint torques. 
The script uses the rtde_control and rtde_receive modules to interface with the UR5, and asyncio to handle concurrent 
communication with the HoloLens.

The main components of the script are:

    comm_robot(): This function establishes a connection with the UR5 and manages its motion based on the received commands.
    comm_hololens(): This function sets up an asyncio server to handle incoming connections and messages from the HoloLens.
    main(): This function combines the robot and HoloLens communication tasks, running them concurrently using asyncio and ThreadPoolExecutor.

The script continuously listens for messages from the HoloLens and processes the received commands to control the UR5 robot.
"""

import asyncio # Import the asyncio library for asynchronous I/O
import socket # Import the socket library for determining IP address
import concurrent.futures # Import the concurrent.futures library for thread-based parallelism
import struct # Import the struct library for working with C-style data structures
import time # Import the struct library for working with C-style data structures

from mock_rtde import MockRTDEControlInterface as RTDEControlInterface
from mock_rtde import MockRTDEReceiveInterface as RTDEReceiveInterface

torques = [0] * 6 # Initialize a list of 6 zeroes to store torque values for each joint
messages = ["DOWN"] # Initialize a list with the initial message "DOWN"
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1) # Create a ThreadPoolExecutor with a single worker

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except:
        return "Error: Unable to get IP address"

def comm_robot():
    rtde_c = RTDEControlInterface("169.254.9.43") # Create a control interface with the robot's IP address
    rtde_r = RTDEReceiveInterface("169.254.9.43") # Create a receive interface with the robot's IP address
    print("Connected to UR5") # Print a message to indicate successful connection to the robot
    up_pose = rtde_r.getActualTCPPose() # Get the current Tool Center Point pose of the robot
    down_pose = up_pose[:] # Create a copy of the current TCP pose for the down pose
    down_pose[2] -= 0.1 # Decrease the z-coordinate of the down pose by 0.1 meters
    while True: 
        global torques # Declare the torques variable as global
        torques = rtde_c.getJointTorques() # Update the torques variable with the current joint torques
        while len(messages) > 0: # While there are messages in the list
            message = messages.pop() # Pop the last message from the list
            print(f'Received Message: {message}')
            if message == "UP": # If the message is "UP"
                rtde_c.stopL(10.0) # Stop the robot's linear motion with a deceleration of 10 m/s^2
                rtde_c.moveL(up_pose, asynchronous=True) # Move the robot to the up_pose asynchronously
            elif message == "DOWN": # If the message is "DOWN"
                rtde_c.stopL(10.0) # Stop the robot's linear motion with a deceleration of 10 m/s^2
                rtde_c.moveL(down_pose, asynchronous=True)  # Move the robot to the down_pose asynchronously
        time.sleep(0.01) # Sleep for 10 milliseconds to reduce CPU usage


async def comm_hololens(): # Define the asynchronous function that communicates with the HoloLens
    async def callback(reader: asyncio.StreamReader, writer: asyncio.StreamWriter): # Define the asynchronous callback function for the HoloLens connection
        print("Connected to HoloLens") 
        while True:
            try:
                message = (await reader.read(1024)).decode() # Read up to 1024 bytes from the reader and decode the message
                if message != " ": # If the message is not empty
                    messages.append(message) # add the message to the messages list to be read by the UR5
                writer.write(struct.pack("!" + "f" * 6, *torques))  # Write the torques list to the writer as a packed binary string, using network byte order ("!") and 6 floating-point values ("f" * 6), one for each torque value in the list. The resulting packed binary string is then written to the writer, which sends the data over the network connection to the HoloLens device.
                await writer.drain() # Wait for the writer to finish sending data
            except:
                break


    await asyncio.start_server(callback, host="0.0.0.0", port=21200) # Start the server, listening on all available network interfaces and using port 21200, with the callback function to handle connections. Note that the host number is basically just the IP address, and the port number refers to a port of communication to host your application on.

async def receive_image(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("Connected to Image Sender")
    while True:
        try:
            # Receive the image size
            image_size_data = await reader.readexactly(4)
            image_size = struct.unpack("!I", image_size_data)[0]

            # Receive the image data
            image_data = await reader.readexactly(image_size)
            
            # Save the received image
            with open("received_image.png", "wb") as img_file:
                img_file.write(image_data)

            # Send an acknowledgment to the sender
            writer.write(b"ACK")
            await writer.drain()

        except asyncio.IncompleteReadError:
            break

async def main():
    print(f"Running on IP: {get_ip_address()}")  # Add this line

    loop = asyncio.get_running_loop()
    await asyncio.gather(
        comm_hololens(),
        loop.run_in_executor(executor, comm_robot),
        asyncio.start_server(receive_image, host="0.0.0.0", port=21201),
    )

if __name__ == "__main__":
    asyncio.run(main())
