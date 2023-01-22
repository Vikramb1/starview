import numpy as np
import matplotlib.pyplot as plt

r = np.linspace(0,360, 200)
y = np.sin(r)

fig, ax = plt.subplots()

ax.scatter(r,y)
ax.set_ylim([-10,10])

plt.show()