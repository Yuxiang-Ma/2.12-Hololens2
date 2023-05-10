"""
Example relay.

Author: Chengyuan Ma
"""

import asyncio
import concurrent.futures
import struct
import time

from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface

torques = [0] * 6
messages = ["DOWN"]
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


def comm_robot():
    rtde_c = RTDEControlInterface("169.254.9.43")
    rtde_r = RTDEReceiveInterface("169.254.9.43")
    print("Connected to UR5")
    up_pose = rtde_r.getActualTCPPose()
    down_pose = up_pose[:]
    down_pose[2] -= 0.1 
    while True:
        global torques
        torques = rtde_c.getJointTorques()
        while len(messages) > 0:
            message = messages.pop()
            if message == "UP":
                rtde_c.stopL(10.0)
                rtde_c.moveL(up_pose, asynchronous=True)
            elif message == "DOWN":
                rtde_c.stopL(10.0)
                rtde_c.moveL(down_pose, asynchronous=True)
        time.sleep(0.01)


async def comm_hololens():
    async def callback(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        print("Connected to HoloLens")
        while True:
            try:
                message = (await reader.read(1024)).decode()
                if message != " ":
                    messages.append(message)
                writer.write(struct.pack("!" + "f" * 6, *torques))
                await writer.drain()
            except:
                break


    await asyncio.start_server(callback, host="0.0.0.0", port=21200)


async def main():
    loop = asyncio.get_running_loop()
    await asyncio.gather(
        comm_hololens(),
        loop.run_in_executor(executor, comm_robot)
    )


if __name__ == "__main__":
    asyncio.run(main())
