from rtde_receive import RTDEReceiveInterface as RTDEReceive

def connect_receive(UR_IP):
    """Connect to the UR5 robot and return the RTDE object.
    This object can be used to read data from the robot.
        args:    UR_IP (str): IP address of the UR5 robot
        returns: rtde_r (RTDEReceive): RTDE object"""
    rtde_r = RTDEReceive(UR_IP)
    # rtde_r.connect()
    print("Connected to UR5")
    return rtde_r

# Aliases
connect_read = connect_receive
get_force = lambda rtde_r: rtde_r.getActualTCPForce()
get_displacement = lambda rtde_r: rtde_r.getActualTCPPose()

if __name__ == '__main__':
    pass