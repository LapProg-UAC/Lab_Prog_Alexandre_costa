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
Z2 = np.cos(R)
Z3 = np.sin(R + np.pi/4)

#Plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z1, cmap='autumn', alpha=0.6, linewidth=0, antialiased=True, shade=True)
ax.plot_surface(X, Y, Z2, cmap='winter', alpha=0.6, linewidth=0, antialiased=True, shade=True)
ax.plot_surface(X, Y, Z3, cmap='cool', alpha=0.6, linewidth=0, antialiased=True, shade=True)

ax.set_title('Superfícies Translúcidas')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.savefig('superficies_translucidas.png', dpi=300)

plt.show()



