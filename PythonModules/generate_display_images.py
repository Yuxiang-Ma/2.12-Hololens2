
import datetime
from time import sleep

import pandas as pd
import matplotlib.pyplot as plt

from config import DATA_PATHS, SAVE_PATHS, IMG_SIZE, DISPLAY_PERIOD, READ_FREQ, UR_IP
from ur5io import connect_read

DPI = 100
N_ROWS = 3


def main():
    while True:
        sleep(READ_FREQ)

        display_data = {}
        for data, pth in DATA_PATHS.items():
            # Read data
            df = pd.read_csv(pth, header=None)
            t = df.values[:, 0]
            v = df.values[:, 1]

            # Filter ROI
            now = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
            read_idx = now - t < DISPLAY_PERIOD

            timestamps = t[read_idx]
            values = v[read_idx]

            # Cache data
            display_data[data] = (timestamps - now, values)

        # Save images
        n_data = len(display_data)
        n_cols = -(n_data // -N_ROWS)
        fig, axs = plt.subplots(N_ROWS, n_cols, figsize=(IMG_SIZE[0]/DPI, IMG_SIZE[1]/DPI))
        for i, data in enumerate(display_data):
            x, y = display_data[data]
            ax = axs[i % N_ROWS, i // N_ROWS]
            ax.plot(x, y, 'o-')
            ax.autoscale()
            ax.grid()
            ax.set_title(data)

        fig.tight_layout()
        plt.savefig(SAVE_PATH, dpi=DPI)
        plt.close('all')


if __name__ == '__main__':
    main()
