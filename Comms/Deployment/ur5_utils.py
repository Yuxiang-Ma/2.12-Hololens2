# First import the library
# import gi
# gi.require_version('Gtk', '2.0')
import pyrealsense2 as rs
import cv2
import numpy as np
import math
import os
from rtde_control import RTDEControlInterface as RTDEControl
import rtde_receive
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import asyncio
import concurrent.futures
import struct
import time
#from ur5_robot_integrate import UR5Robot

async def plot_data(fig, axs, ts, forces, displacements, ROI=int(DISPLAY_PERIOD/READ_FREQ), save=True):
    """Update plot with current data from the UR5 robot.
        args:    fig (Figure): figure object
                 axs (Axes): axes object
                 ts (list): list of timestamps
                 forces (list): list of forces
                 displacements (list): list of displacements
        kwargs:  ROI (int): number of data points to display
                 save (bool): if True, save the figure
        returns: None"""
    # Convert to numpy arrays
    #ts = np.array(ts)
    #forces = np.array(forces)
    #displacements = np.array(displacements)

    # Plot
    axs[0].plot(ts, forces)
    axs[0].set_title("Force")
    axs[0].grid()
    axs[1].plot(ts, displacements)
    axs[1].set_title("Displacement")
    axs[1].grid()
    #fig.tight_layout()
    plt.draw()
    #plt.pause(PAUSE_TIME)
    if save:
        plt.savefig(SAVE_PATH, dpi=DPI)

def rs_to_ur5(x_rs, y_rs, z_rs):
    #converts from realsense coords to ur5 coords
    #x_rs, y_rs, z_rs, inputs in MILLIMETERS
    x_ur5 = 0
    y_ur5 = 0
    z_ur5 = 0

    #Transformation 1: Rotation about z1 by -70 degrees
    theta1 = math.radians(70)
    Rz_theta1 = [[math.cos(theta1), -math.sin(theta1), 0], [math.sin(theta1), math.cos(theta1), 0], [0, 0, 1]]

    #Transformation 2: Rotation about x2 by -131 degrees
    theta2 = math.radians(131) 
    Rx_theta2 = [[1, 0, 0],[0, math.cos(theta2), -math.sin(theta2)], [0, math.sin(theta2), math.cos(theta2)]]

    #full rotation matrix
    Rzx = np.matmul(Rx_theta2, Rz_theta1)
    print("Rzx", Rzx)
    Rzx_inv = np.linalg.inv(Rzx)
    [[x_ur5], [y_ur5], [z_ur5]] = np.matmul(Rzx_inv, [[x_rs], [y_rs], [z_rs]])
    print("un_translated",(x_ur5,y_ur5,z_ur5))

    #Transformation 3: Translation
    x_ur5 = x_ur5 - 360 #mm
    y_ur5 = y_ur5 - 834 #mm
    z_ur5 = z_ur5 + 579 #mm

    return [-x_ur5+80, y_ur5+140, z_ur5+80]

def move_ur5_to_start():
    """
    This function captures frames from a RealSense camera, finds contours of a triangular object, 
    and calculates the average position of the object's center. The function then converts the 
    position to UR5 coordinates and stores the result in a list.
    """
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    # Configure streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # Start streaming
    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    def nothing(x):
        # any operation
        pass

    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
    cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
    cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
    cv2.createTrackbar("U-H", "Trackbars", 3, 180, nothing)
    cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)

    font = cv2.FONT_HERSHEY_COMPLEX
    align_to=rs.stream.color
    align=rs.align(align_to)

    state = 0

    x_input = []
    y_input = []
    z_input = []

    while state < 100:

        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        depth_stream = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
        
        #get intrinsics of camera
        intr = depth_stream.get_intrinsics()
        
        depth_image = np.array(aligned_depth_frame.get_data())
        color_image = np.array(color_frame.get_data())

        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("L-H", "Trackbars")
        l_s = cv2.getTrackbarPos("L-S", "Trackbars")
        l_v = cv2.getTrackbarPos("L-V", "Trackbars")
        u_h = cv2.getTrackbarPos("U-H", "Trackbars")
        u_s = cv2.getTrackbarPos("U-S", "Trackbars")
        u_v = cv2.getTrackbarPos("U-V", "Trackbars")

        lower_red = np.array([l_h, l_s, l_v])
        upper_red = np.array([u_h, u_s, u_v])

        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask1, kernel)
        #mask = cv2.dilate(mask1, kernel)
        
        

        # Contours detection
        if int(cv2.__version__[0]) > 3:
            # Opencv 4.x.x
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            # Opencv 3.x.x
            _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)

            if area > 400:
                cv2.drawContours(color_image, [approx], 0, (0, 0, 0), 5)

                if len(approx) == 3: #if contour is a triangle
                    #find center point of shape
                    M = cv2.moments(cnt)
                    if M['m00'] != 0.0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])
                        distance = aligned_depth_frame.get_distance(x,y) #in m
                        cv2.putText(color_image, str(distance), (x,y), font, 1, (0, 0, 0)) #put distance value on center of shape

                    #convert x,y center coords to real world mm coords
                    [x_real, y_real, z_real] = rs.rs2_deproject_pixel_to_point(intr, [x, y], distance)
                    #print(intr)
                    #print([x_real, y_real, z_real])


                    [x_ur5, y_ur5, z_ur5] = rs_to_ur5(x_real*1000, y_real*1000, distance*1000)
                    state = state +1
                    print("==========================", state, '=========================')
                    x_input.append(x_ur5)
                    y_input.append(y_ur5)
                    z_input.append(z_ur5)

                    #print([x_ur5, y_ur5, z_ur5])


                        
        cv2.imshow("Frame", color_image)
        cv2.imshow("Mask", mask)

        key = cv2.waitKey(1)
        if key == 27:
            break
        sleep(.1)

    cv2.destroyAllWindows()

    x_input = np.array(x_input)
    y_input = np.array(y_input)
    z_input = np.array(z_input)

    x_avg = np.mean( x_input[-10:] ) / 1000
    y_avg = np.mean( y_input[-10:] ) / 1000
    z_avg = np.mean( z_input[-10:] ) / 1000




    print(x_avg, y_avg, z_avg)

    z_avg = z_avg + 0.005

    r = [x_avg, y_avg, z_avg, -56.68* 2*3.1415/360.0, 90.52* 2*3.1415/360.0, 53.1* 2*3.1415/360.0]
    
    return r


def start_ur5_action(r,pump_period=550,plot_flag=True,ur5_ip="169.254.9.43"):
    """
    Executes a control loop for the UR5 robot. Moves the robot to an initial position, applies a sine wave force, 
    and records the force exerted and the position of the robot. The robot is controlled using the RTDE interface.
    """

    SAVE_PATH = "/home/ur5-2/roboresponse/manipulator/display_image.png" #"../img/display_image.png"
    DISPLAY_PERIOD = 10  # seconds
    READ_FREQ = 0.5  # seconds
    DPI = 100
    N_ROWS = 2
    IMG_SIZE = (640, 480)  # (width, height)
    PAUSE_TIME = 0.0000000001
    UR5IP = "169.254.9.43"

    rtde_c = RTDEControl(UR5IP)
    rtde_r = rtde_receive.RTDEReceiveInterface(UR5IP)


    task_frame = [0, 0, 0, 0, 0, 0]
    selection_vector = [0, 0, 1, 0, 0, 0]
    wrench_down = [0, 0, -150, 0, 0, 0] #tried up to 500, same as 150
    wrench_up = [0, 0, 10, 0, 0, 0]
    force_type = 2
    limits = [2, 2, 1.5, 1, 1, 1]
    #joint_q = [-1.54, -1.83, -2.28, -0.59, 1.60, 0.023]
    #joint_q = [-36.24* 2*3.1415/360.0, -102* 2*3.1415/360.0, -125.1* 2*3.1415/360.0, -41.09* 2*3.1415/360.0, 90.45* 2*3.1415/360.0, 53.1* 2*3.1415/360.0]


    joint_q = [68.59* 2*3.1415/360.0, -52.65* 2*3.1415/360.0, 91.33* 2*3.1415/360.0, -130.73* 2*3.1415/360.0, 270.82* 2*3.1415/360.0, 119.09* 2*3.1415/360.0]

    #This is downstairs
    #joint_q = [-36.21* 2*3.1415/360.0, -92.47* 2*3.1415/360.0, -118.24* 2*3.1415/360.0, -56.68* 2*3.1415/360.0, 90.52* 2*3.1415/360.0, 53.1* 2*3.1415/360.0]

    #joint_q = joint_q * 2*3.1415/360.0

    # Move to initial joint position with a regular moveJ
    # rtde_c.moveJ(joint_q, 1.50, 1.4, True)
    rtde_c.moveL(r, 1.50, 1.4, True)

    sleep(2.5)
    #rtde_c.stopJ(0.5)

    speed = [0, 0, -0.050, 0, 0, 0]
    rtde_c.moveUntilContact(speed)

    #get jacobian
    #smoother motion
    #can we control joint angles/velocities directly? wihtout using the moveJ
    #what is maximum force we can exert on body? is it still 10N or has this been increased


    #rtde_c.forceModeSetDamping(0.7)

    amp = 200

    t_out = []
    force_out = []
    pos_out = []

    fig, axs = plt.subplots(N_ROWS, 1, figsize=(IMG_SIZE[0]/DPI, IMG_SIZE[1]/DPI))
    loop = asyncio.get_event_loop()

    task_frame = [0, 0, 0, 0, 0, 0]
    selection_vector = [0, 0, 1, 0, 0, 0]
    force_type = 2
    limits = [2, 2, 1, 1, 1, 1]

    T = pump_period
    t0 = 0

    # Execute 500Hz control loop for 4 seconds, each cycle is 2ms
    for i in range(10000):
        t_start = rtde_c.initPeriod()
        

        sine_target = - np.abs(amp*np.sin(2*np.pi*i/T))+100
        #print(sine_target)
        wrench_up = [0, 0, sine_target, 0, 0, 0]

        rtde_c.forceMode(task_frame, selection_vector, wrench_up, force_type, limits)

        pos_cur = rtde_r.getActualTCPPose()
        #t0 += t_start
        #t_out.append(t)
        force_out.append(np.linalg.norm(rtde_r.getActualTCPForce()[2]))
        #pos_out.append(initial_target_z - z_val_cur)

        if plot_flag:
            loop.run_until_complete(plot_data(fig, axs, t_out[-5:], force_out[-5:], pos_out[-5:]))
        
        rtde_c.waitPeriod(t_start)


    #fig, ax = plt.subplots()
    #ax.plot(t_out, force_out)

    #ax.set(xlabel='time (s)', ylabel='force', title='force')
    #ax.grid()

    #fig.savefig("force.png")
    #plt.show()

    #plt.figure(1)
    #fig2, ax2 = plt.subplots()
    #ax2.plot(t_out, pos_out)

    #ax2.set(xlabel='time (s)', ylabel='pos',title='pos')
    #ax2.grid()

    #fig2.savefig("position.png")
    #plt.show()


    #rtde_c.forceModeStop()
    rtde_c.stopScript()



