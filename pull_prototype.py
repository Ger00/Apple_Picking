import time
from pathlib import Path

import numpy as np
from numpy.lib.shape_base import array_split

# Opens the file for reading.
# If it does not exist, yet, the file is created.
# The depth data is in a single array of 64 elements.
dataPath = Path("distance.sensorData")
if dataPath.is_file():
    sensorFile = open(dataPath,'rb')
else:
    sensorFile = open(dataPath,'xb')
    # Populates the new file with dummy data.
    dummyList = []
    for n in range(64):
        dummyList.append(0)
    dummyArray = np.array(dummyList, np.int16)
    sensorFile.write(bytearray(dummyArray))
    print("Created new file.")
    quit()

sensorDistanceBinary = bytearray(sensorFile.read(1024))
sensorDistanceInt = []
for n in range(1,1010,16):
    sensorDistanceInt.append(int.from_bytes(sensorDistanceBinary[n:n+15]))
sensorDistanceInt16 = np.array(sensorDistanceInt, np.int16)

# Defines sleep_time for later. This helps with the 60hz refresh rate.
sleep_time = 166_666_667

# The 'try' statement is there to handle errors.
try:
    # An infinite loop. It will run until someone stops the software, or until an error occurs.
    while True:
        # Saves the start time of this iteration, to calculate the sleep time at the end.
        start_time = time.process_time_ns()

        # Creates an array of 8 arrays, which each contain 8 depth values.
        # This is to represent the data in an 8x8 format.
        array8x8 = np.array(array_split(sensorDistanceInt16, 8))

        # Prints the depth map.
        print(array8x8)

        # Calculates the wait time until the next iteration.
        sleep_time = 166_666_667 + start_time - time.process_time_ns()
        # Pauses the program, so that it only runs once every 1/60 of a second.
        time.sleep(sleep_time / 1_000_000_000.0)

# Prints a message, if a ValueError occurs.
except ValueError:
    # If the iteration takes longer than 1/60 of a second, the program prints the following message:
    if sleep_time < 0:
        print("This iteration took longer than 1/60 of a second, by " + str(-sleep_time) + " nanoseconds.")
    # If the array does not contain exactly 64 elements:
    elif len(sensorDistanceInt16) != 64:
        print("Unexpected array length: " + str(len(sensorDistanceInt16)))
    # In any other case it prints this:
    else:
        print("Unexpected ValueError")
