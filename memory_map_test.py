import time
import numpy as np
from numpy.lib.shape_base import array_split

# Creates a new memory-mapped file.
# The depth data is in a single array of 64 elements.
sensorDistance = np.memmap(filename="distance.dat", dtype=np.int16, mode='w+', shape=64)

# Defines sleep_time for later. This helps with the 60hz refresh rate.
sleep_time = 166_666_667

# The 'try' statement is there to handle errors.
try:
    # An infinite loop. It will run until someone stops the software, or until an error occurs.
    while True:
        # Saves the start time of this iteration, to calculate the sleep time at the end.
        start_time = time.process_time_ns()

        # Reads all depth data from the memory-mapped file.
        sensorDistance = np.memmap(filename="distance.dat", dtype=np.int16, mode='r', shape=64)

        # Creates an array of 8 arrays, which each contain 8 depth values.
        # This is to represent the data in an 8x8 format.
        # The values will not be in the correct order. I will add that later.
        newArray = np.array(array_split(sensorDistance, 8))

        # Prints the depth map. This will only show zeroes, if there is no sensor.
        print(newArray)

        # Calculates the wait time until the next iteration.
        sleep_time = 166_666_667 + start_time - time.process_time_ns()
        # Pauses the program, so that it only runs once every 1/60 of a second.
        time.sleep(sleep_time / 1_000_000_000.0)

# Prints a message, if a ValueError occurs.
except ValueError:
    # If the iteration takes longer than 1/60 of a second, the program prints the following message:
    if sleep_time < 0:
        print("This iteration took longer than 1/60 of a second, by " + str(-sleep_time) + " nanoseconds.")
    # In any other case it prints this:
    else:
        print("Unexpected ValueError")
