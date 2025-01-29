# This code does the following
# Creating a simulation rock data with spheres in it.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random

# Box dimensions
box_size = 10
num_circles = 50
initial_radius = box_size / 10  # r = 1/10 of the side length

# Generate random positions for 5 circles
circles = []
for _ in range(num_circles):
    x, y, z = np.random.uniform(initial_radius, box_size - initial_radius, 3)
    circles.append([x, y, z, initial_radius])

# Function to check if two circles touch or overlap
def circles_touch(c1, c2):
    x1, y1, z1, r1 = c1
    x2, y2, z2, r2 = c2
    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
    return distance <= (r1 + r2)

# Grow circles until they touch
growing = [True] * num_circles  # Keep track of which circles are still growing
growth_rate = 0.1  # Rate at which radius increases

while any(growing):
    for i in range(num_circles):
        if not growing[i]:
            continue
        # Temporarily grow the circle
        circles[i][3] += growth_rate  
        # Check for collisions
        for j in range(num_circles):
            if i != j and circles_touch(circles[i], circles[j]):
                growing[i] = False  # Stop growing this circle
                circles[i][3] -= growth_rate  # Undo last growth step
                break

# Visualization
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the circles
for x, y, z, r in circles:
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    xs = r * np.cos(u) * np.sin(v) + x
    ys = r * np.sin(u) * np.sin(v) + y
    zs = r * np.cos(v) + z
    ax.plot_wireframe(xs, ys, zs, color='b')

# Set limits
ax.set_xlim([0, box_size])
ax.set_ylim([0, box_size])
ax.set_zlim([0, box_size])

# Show the plot
plt.show()
