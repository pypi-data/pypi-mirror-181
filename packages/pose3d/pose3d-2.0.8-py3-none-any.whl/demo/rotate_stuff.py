import numpy as np

from pathlib import Path
from sys import path
path.append(Path(__file__).parent.parent.as_posix())

from pose3d import ER

matrix = np.array([[2, 3, 4], [1, 2, 3], [5, 6, 7]])

rotation = ER(dim=3)

rotation.from_matrix(matrix)
x_angle, y_angle, z_angle = rotation.as_euler('xyz', degrees=True)

print(x_angle)
print(rotation.roll(degrees=True))
print(y_angle)
print(rotation.pitch(degrees=True))
print(z_angle)
print(rotation.yaw(degrees=True))
