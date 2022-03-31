import yfinance as yf 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('bmh')

ticker = 'AAPL'
data = yf.download(ticker, period='1y', interval='1d', auto_adjust=True, progress=False)

fig, ax = plt.subplots(figsize=(12,6))
x = 0
y = 0
ax.plot(x,y)
fig.suptitle(ticker, fontsize=20, fontweight='bold')
plt.tight_layout()

def animation(frame):
    x = data.index[0: int(frame)]
    y = data.Close[0: int(frame)]
    plt.cla()
    ax.plot(x, y)
    if len(x) >= 2:
        d1 = x[0].strftime('%Y-%m-%d')
        d2 = x[-1].strftime('%Y-%m-%d')
        ax.set_title(f"From [{d1}] to [{d2}]\nTotal days: {len(x)}", loc='left')
    fig.suptitle(ticker, fontsize=20, fontweight='bold')
    
animate = FuncAnimation(fig, animation, frames=len(data), interval=int(len(data)/4))
animate.save('stock.gif', dpi=200)
