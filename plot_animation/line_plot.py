import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.animation import FuncAnimation

plt.style.use('bmh')

x = np.random.random(size=(100,))
y = np.zeros(100)

fig, ax = plt.subplots()
line,  = ax.plot(x, y)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title('Slope=0')
plt.tight_layout()

def animated(frame):
    y = frame/100 * x
    line.set_data((x, y))
    ax.set_title(f'Slope={frame/100:.2f}')
    
animation = FuncAnimation(fig, animated, frames=100, interval=50)
animation.save('line.gif', dpi=200)