import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


Rest_Positions = np.genfromtxt('workspace/rest_position.txt', delimiter = ',')
target1 = Rest_Positions[0]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.plot(target1)
ax.plot(target1[0],target1[1],target1[2])