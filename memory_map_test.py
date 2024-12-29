import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.shape_base import array_split

# Reads from memory-mapped file, or (if it does not exist) creates a new file.
# The depth data is in a single array of 64 elements.
sensorDistance = np.memmap(filename="distance.dat", dtype=np.int16, mode='w+', shape=64)

# Creates an array of 8 arrays, which each contain 8 depth values.
# This is to represent the data in an 8x8 format.
# The values will not be in the correct order. I will add that later.
newArray = np.array(array_split(sensorDistance, 8))

# Creates a depth map.
figure = plt.figure()
axes = figure.add_axes([0,0,1,1])
axes.imshow(newArray)

# Shows the depth map. This will only show one color, because all values are 0.
plt.show()
