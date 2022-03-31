import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.animation import FuncAnimation

plt.style.use('bmh')

x = np.linspace(0, 2*np.pi, 100)
y = np.zeros(100)

fig, ax = plt.subplots()
line,  = ax.plot(x, y)
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.1, 1.1)
plt.tight_layout()

def animation_function(frame):
    y = np.cos(x + 2*np.pi*frame/100)
    line.set_data((x, y))

animated = FuncAnimation(fig, animation_function, frames=100, interval=10)
animated.save('cos.gif', dpi=300)