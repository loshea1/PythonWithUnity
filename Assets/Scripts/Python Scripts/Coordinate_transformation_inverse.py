import numpy as np
import math


def eulerAnglesToRotationMatrix():
# Old position
    # theta = [2.355,0,0]
    # translate = [0, 0.4, 0.5]
    theta = [1,0,0]
    translate = [0, -0.42,0.28]
    R_x = np.array([[1, 0, 0, 0],
                    [0, math.cos(theta[0]), -math.sin(theta[0]), 0],
                    [0, math.sin(theta[0]), math.cos(theta[0]), 0],
                    [0, 0, 0, 1]
                    ])

    R_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1]), 0],
                    [0, 1, 0, 0],
                    [-math.sin(theta[1]), 0, math.cos(theta[1]), 0],
                    [0, 0, 0, 1]
                    ])

    R_z = np.array([[math.cos(theta[2]), -math.sin(theta[2]), 0, 0],
                    [math.sin(theta[2]), math.cos(theta[2]), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                    ])
    rotation = np.dot(R_z, np.dot(R_y, R_x))
    translation = np.array([[1, 0, 0, translate[0]],
                            [0, 1, 0, translate[1]],
                            [0, 0, 1, translate[2]],
                            [0, 0, 0, 1]
                            ])

    matrix_transformation = np.dot(np.transpose(rotation),np.transpose(-translation))
    return matrix_transformation
