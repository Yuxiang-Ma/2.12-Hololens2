from rtde_control import RTDEControlInterface as RTDEControl
import rtde_receive
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import asyncio
import concurrent.futures
import struct

SAVE_PATH = "~/display_image.png" #"../img/display_image.png"
DISPLAY_PERIOD = 10  # seconds
READ_FREQ = 0.5  # seconds
DPI = 100
N_ROWS = 2
IMG_SIZE = (640, 480)  # (width, height)
PAUSE_TIME = 0.0000000001

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

rtde_c = RTDEControl("169.254.9.43")
rtde_r = rtde_receive.RTDEReceiveInterface("169.254.9.43")

task_frame = [0, 0, 0, 0, 0, 0]
selection_vector = [0, 0, 1, 0, 0, 0]
wrench_down = [0, 0, -150, 0, 0, 0] #tried up to 500, same as 150
wrench_up = [0, 0, 10, 0, 0, 0]
force_type = 2
limits = [2, 2, 1.5, 1, 1, 1]
#joint_q = [-1.54, -1.83, -2.28, -0.59, 1.60, 0.023]
#joint_q = [-36.24* 2*3.1415/360.0, -102* 2*3.1415/360.0, -125.1* 2*3.1415/360.0, -41.09* 2*3.1415/360.0, 90.45* 2*3.1415/360.0, 53.1* 2*3.1415/360.0]
joint_q = [68.59* 2*3.1415/360.0, -52.65* 2*3.1415/360.0, 91.33* 2*3.1415/360.0, -130.73* 2*3.1415/360.0, 270.82* 2*3.1415/360.0, 119.09* 2*3.1415/360.0]
#joint_q = joint_q * 2*3.1415/360.0

# Move to initial joint position with a regular moveJ
rtde_c.moveJ(joint_q, 1.50, 1.4, True)
sleep(2.5)
#rtde_c.stopJ(0.5)

speed = [0, 0, -0.050, 0, 0, 0]
rtde_c.moveUntilContact(speed)

#get jacobian
#smoother motion
#can we control joint angles/velocities directly? wihtout using the moveJ
#what is maximum force we can exert on body? is it still 10N or has this been increased​

#rtde_c.forceModeSetDamping(0.7)​
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

T = 550
t0 = 0

# Execute 500Hz control loop for 4 seconds, each cycle is 2ms
for i in range(10000):
    t_start = rtde_c.initPeriod()
    

    sine_target = - np.abs(amp*np.sin(2*np.pi*i/T))+100
    print(sine_target)
    wrench_up = [0, 0, sine_target, 0, 0, 0]

    rtde_c.forceMode(task_frame, selection_vector, wrench_up, force_type, limits)

    pos_cur = rtde_r.getActualTCPPose()
    #t0 += t_start
    #t_out.append(t)
    force_out.append(np.linalg.norm(rtde_r.getActualTCPForce()[2]))
    #pos_out.append(initial_target_z - z_val_cur)


    #loop.run_until_complete(plot_data(fig, axs, t_out[-5:], force_out[-5:], pos_out[-5:]))
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
