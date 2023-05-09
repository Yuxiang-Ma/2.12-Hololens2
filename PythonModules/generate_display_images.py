import random#, datetime
from time import sleep, time

import numpy as np
import matplotlib.pyplot as plt

from config import SAVE_PATH, IMG_SIZE, DISPLAY_PERIOD, READ_FREQ, UR_IP
# from ur5io import connect_read, get_force, get_displacement

DPI = 100
N_ROWS = 3
PAUSE_TIME = 0.1

# Set to True to connect to the robot
ROBOT_ACTIVE = False


def update_data(rtde_r, start, ts, forces, displacements, test=False):
    """Update data lists with current data from the UR5 robot.
        args:    rtde_r (RTDEReceive): RTDE object
                 start (float): start time
                 ts (list): list of timestamps
                 forces (list): list of forces
                 displacements (list): list of displacements
        kwargs:  test (bool): if True, generate random data instead of reading from the robot
        returns: None"""
    # Append current data to lists
    ts.append(time() - start)
    if test:
        forces.append(random.expovariate(1/10))
        displacements.append([random.expovariate(1/10), random.expovariate(1/10)])
    else:
        forces.append(get_force(rtde_r))
        displacements.append(get_displacement(rtde_r))


def plot_data(ts, forces, displacements, ROI=int(DISPLAY_PERIOD/READ_FREQ), save=False, relative=True):
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
    ts = np.array(ts)
    forces = np.array(forces)
    displacements = np.array(displacements)

    # Plot
    fig, axs = plt.subplots(N_ROWS, 1, figsize=(IMG_SIZE[0] / DPI, IMG_SIZE[1] / DPI))

    ts_plot = ts[-ROI:]
    if relative:
        ts_plot -= ts[-1]

    axs[0].plot(ts_plot, forces[-ROI:])
    axs[0].set_title("Force")
    axs[0].grid()
    axs[1].plot(ts_plot, displacements[-ROI:, 0])
    axs[1].set_title("Displacement X")
    axs[1].grid()
    axs[2].plot(ts_plot, displacements[-ROI:, 1])
    axs[2].set_title("Displacement Y")
    axs[2].grid()
    fig.tight_layout()
    if save:
        plt.savefig(SAVE_PATH, dpi=DPI)
    else:
        plt.show()


def main(test=False):
    """Main function."""
    # Connect to UR5 and initialize data
    rtde_r = connect_read(UR_IP) if not test else None
    start = time()
    ts            = []
    forces        = []
    displacements = []

    # Main loop
    while True:
        sleep(READ_FREQ)
        update_data(rtde_r, start, ts, forces, displacements, test=test)
        plot_data(ts, forces, displacements, save=True, relative=True)
        plt.close('all')

    if ROBOT_ACTIVE:
        rtde_r.disconnect()


if __name__ == '__main__':
    main(test=True)
