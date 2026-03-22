import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import time

S = 5
lambda_rate = 5
N = 5
sigma = 1.5
min_call = 1
max_call = 10
queue_max = 10
sim_time = 50

channels = [0]*S
queue = deque()
served = 0
rejected = 0
waits = []
queue_lens = []
rho = []
Q = []
W = []

arrivals, calls = [], []
t = 0
while t < sim_time:
    t += np.random.exponential(1/lambda_rate)
    if t >= sim_time: break
    dur = int(np.clip(np.random.normal(N,sigma), min_call, max_call))
    arrivals.append(int(t))
    calls.append(dur)

plt.ion()
fig, axs = plt.subplots(3,1,figsize=(6,6))
fig.show()
fig2, ax_channels = plt.subplots(figsize=(4,3))
ax_channels.set_xlim(0,2)
ax_channels.set_ylim(0,S)
ax_channels.axis('off')
fig2.show()


for t in range(sim_time):
    for idx,(a,dur) in enumerate(zip(arrivals,calls)):
        if a==t:
            free = next((i for i,c in enumerate(channels) if c<=0),None)
            if free is not None:
                channels[free] = dur
                waits.append(0)
                served += 1
            elif len(queue) < queue_max:
                queue.append((t,dur))
            else:
                rejected += 1

    for i in range(S):
        if channels[i]>0: channels[i]-=1
    for i in range(S):
        if channels[i]<=0 and queue:
            t0,dur = queue.popleft()
            waits.append(t - t0)
            channels[i] = dur
            served += 1

    rho.append(min(1, lambda_rate * N / S))
    queue_lens.append(len(queue))
    Q.append(np.mean(queue_lens))
    W.append(np.mean(waits) if waits else 0)

    for ax in axs: ax.clear()
    axs[0].plot(rho,color='green'); axs[0].set_title("Ro")
    axs[1].plot(Q,color='red'); axs[1].set_title("Q")
    axs[2].plot(W,color='blue'); axs[2].set_title("W")
    fig.canvas.draw(); fig.canvas.flush_events()


    ax_channels.clear()
    ax_channels.axis('off')
    for i,c in enumerate(channels):
        color = 'red' if c>0 else 'green'
        ax_channels.barh(i,1,color=color)
        if c>0:
            ax_channels.text(0.5,i,f"{c}s",ha='center',va='center',color='white')
    fig2.canvas.draw(); fig2.canvas.flush_events()

    time.sleep(0.05)


print(f"\nSymulacja zakończona po {sim_time} krokach")
print(f"Obsłużeni: {served}, Odrzuceni: {rejected}")
print("Ro\tQ\tW")
with open("wyniki.txt","w",encoding="utf-8") as f:
    f.write(f"Kanały:{S}\nLambda:{lambda_rate}\nN:{N}\nSigma:{sigma}\nMin:{min_call}\nMax:{max_call}\nKolejka:{queue_max}\nCzas:{sim_time}\n\n")
    f.write("Ro\tQ\tW\n")
    for r,q,w in zip(rho,Q,W):
        f.write(f"{r:.4f}\t{q:.4f}\t{w:.4f}\n")
        print(f"{r:.4f}\t{q:.4f}\t{w:.4f}")
print("Wyniki zapisano do wyniki.txt")