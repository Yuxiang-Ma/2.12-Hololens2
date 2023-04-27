from rtde_receive import RTDEReceiveInterface as RTDEReceive
import pandas as pd
import matplotlib.pyplot as plt

# Set IP address of the UR5 robot
# UR_IP = "169.254.9.43"

def connect_receive(UR_IP):
    """Connect to the UR5 robot and return the RTDE object."""
    rtde_r = RTDEReceive(UR_IP)
    rtde_r.connect()
    print("Connected to UR5")
    setattr(rtde_r, 'get_force', lambda: rtde_r.getActualTCPForce())
    setattr(rtde_r, 'get_displacement', lambda: rtde_r.getActualTCPPose())
    return rtde_r
connect_read = connect_receive

# OLD CODE below, replaced with setattr statements above
# def get_force(rtde_r):
#     return rtde_r.getActualTCPForce()

# def get_displacement(rtde_r):
#     return rtde_r.getActualTCPPose()
