
import datetime, random
from time import sleep, time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import DATA_PATHS, SAVE_PATH, IMG_SIZE, DISPLAY_PERIOD, READ_FREQ, UR_IP
from ur5io import connect_read

DPI = 100
N_ROWS = 3

ROBOT_ACTIVE = True

def update_data(rtde_r, start, ts, forces, displacements, test=False):
    """Update data lists with current data from the UR5 robot.
        args:    rtde_r (RTDEReceive): RTDE object
                 timestamps (list): list of timestamps
                 forces (list): list of forces
                 displacements (list): list of displacements
        returns: None"""
    # Append current data to lists
    ts.append(time() - start)
    if test:
        forces.append(random.expovariate(1/10))
        displacements.append([random.expovariate(1/10), random.expovariate(1/10)])
    else:
        forces.append(rtde_r.get_force())
        displacements.append(rtde_r.get_displacement())

def plot_data(ts, forces, displacements, ROI=10):
    """Plot data from the UR5 robot.
        args:    timestamps (list): list of timestamps
                 forces (list): list of forces
                 displacements (list): list of displacements
                 ROI (int): time window to plot
        returns: None"""
    # Convert to numpy arrays
    ts = np.array(ts)
    forces = np.array(forces)
    displacements = np.array(displacements)

    # Plot
    fig, axs = plt.subplots(3, 1, figsize=(IMG_SIZE[0]/DPI, IMG_SIZE[1]/DPI))
    axs[0].plot(ts[-ROI:], forces[-ROI:])
    axs[0].set_title("Force")
    axs[0].grid()
    axs[1].plot(ts[-ROI:], displacements[-ROI:, 0])
    axs[1].set_title("Displacement X")
    axs[1].grid()
    axs[2].plot(ts[-ROI:], displacements[-ROI:, 1])
    axs[2].set_title("Displacement Y")
    axs[2].grid()
    fig.tight_layout()
    plt.show()


def main(test=False):
    # Connect to UR5 and initialize data lists
    rtde_r = connect_read(UR_IP) if not test else None
    start = time()
    ts = []
    forces = []
    displacements = []

    while True:
        sleep(READ_FREQ)

        if ROBOT_ACTIVE:
            update_data(rtde_r, start, ts, forces, displacements, test=test)
            plot_data(ts, forces, displacements)

        # display_data = {}
        # for data, pth in DATA_PATHS.items():
        #     # Read data
        #     df = pd.read_csv(pth, header=None)
        #     t = df.values[:, 0]
        #     v = df.values[:, 1]

        #     # Filter ROI
        #     now = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
        #     read_idx = now - t < DISPLAY_PERIOD

        #     timestamps = t[read_idx]
        #     values = v[read_idx]

        #     # Cache data
        #     display_data[data] = (timestamps - now, values)

        # # Save images
        # n_data = len(display_data)
        # n_cols = -(n_data // -N_ROWS)
        # fig, axs = plt.subplots(N_ROWS, n_cols, figsize=(IMG_SIZE[0]/DPI, IMG_SIZE[1]/DPI))
        # for i, data in enumerate(display_data):
        #     x, y = display_data[data]
        #     ax = axs[i % N_ROWS, i // N_ROWS]
        #     ax.plot(x, y, 'o-')
        #     ax.autoscale()
        #     ax.grid()
        #     ax.set_title(data)

        # fig.tight_layout()
        # plt.savefig(SAVE_PATH, dpi=DPI)
        # plt.close('all')


if __name__ == '__main__':
    main(test=True)
