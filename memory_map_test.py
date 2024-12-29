import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.shape_base import array_split

sensorDistance = np.memmap(filename="distance.dat", dtype=np.int16, mode='w+', shape=64)
newArray = np.array(array_split(sensorDistance, 8))
figure = plt.figure()
axes = figure.add_axes([0,0,1,1])
axes.imshow(newArray)
plt.show()
