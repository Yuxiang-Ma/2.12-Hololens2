
import datetime
from time import sleep

import numpy as np


# Imaginary Torque Configuration
A = [2, 3, 4, 7, 1, 5]
W = [5, 2, 1, 5, 3, 4]


def main():
    while True:
        t = datetime.datetime.now(tz=datetime.timezone.utc).timestamp()

        for i in range(6):
            torque = A[i] * np.sin(W[i]*t)

            with open(f'./ur5_torque{i}.csv', 'a') as file:
                file.write(f'{t}, {torque}\n')

        sleep(1.0)


if __name__ == '__main__':
    main()
