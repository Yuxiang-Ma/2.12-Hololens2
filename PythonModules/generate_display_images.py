
import datetime
from time import sleep
import pytz

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md

from config import DATA_PATHS, SAVE_PATHS, IMG_SIZE, DISPLAY_PERIOD, READ_FREQ

TZ_EST = pytz.timezone('US/Eastern')
XFMT = md.DateFormatter('%H:%M:%S', TZ_EST)
DPI = 100


while True:
    sleep(READ_FREQ)

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
        
        # Convert UTC timestamp to EST
        dates=[datetime.datetime.fromtimestamp(ts) for ts in timestamps]
        datenums=md.date2num(dates)
        
        # Save images
        plt.figure(figsize=(IMG_SIZE[0]/DPI, IMG_SIZE[1]/DPI))
        plt.plot(datenums, values, 'o-')
        plt.xticks(rotation=25)
        ax = plt.gca()
        ax.xaxis.set_major_formatter(XFMT)
        plt.autoscale()
        plt.savefig(SAVE_PATHS[data], dpi=DPI)        
