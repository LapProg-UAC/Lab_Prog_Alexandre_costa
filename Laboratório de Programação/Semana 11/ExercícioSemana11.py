import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Meshgrid
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

#Radial coordinates
R = np.sqrt(X**2 + Y**2)

#Surfaces
Z1 = np.sin(R)
Z_plane = np.zeros_like(X)

#Plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z1, cmap='plasma', alpha=0.8, linewidth=0, antialiased=True, shade=True)
ax.plot_surface(X, Y, Z_plane, cmap='Blues', alpha=0.3, linewidth=0, antialiased=True, shade=True)
ax.contour(X, Y, Z1, 25, offset=0, cmap='inferno')

ax.set_title('Superfícies Translúcidas')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.savefig('superficies_translucidas.png', dpi=300)

plt.show()


