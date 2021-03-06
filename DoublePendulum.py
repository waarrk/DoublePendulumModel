#!/usr/bin/env python
# coding: utf-8

# In[1]:

from numpy import sin, cos
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


G = 9.8     # 重力加速度 [m/s^2]
L1 = 1.0    # 単振り子1の長さ [m]
L2 = 0.3    # 単振り子2の長さ [m]
M1 = 2.5    # おもり1の質量 [kg]
M2 = 0.3    # おもり2の質量 [kg]


# In[3]:


# 運動方程式
def derivs(t, state):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    delta = state[2] - state[0]
    den1 = (M1+M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
    dydx[1] = ((M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                + M2 * G * sin(state[2]) * cos(delta)
                + M2 * L2 * state[3] * state[3] * sin(delta)
                - (M1+M2) * G * sin(state[0])) / den1)

    dydx[2] = state[3]

    den2 = (L2/L1) * den1
    dydx[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                + (M1+M2) * G * sin(state[0]) * cos(delta)
                - (M1+M2) * L1 * state[1] * state[1] * sin(delta)
                - (M1+M2) * G * sin(state[2]))
               / den2)

    return dydx


# In[4]:


# 時間生成
t_span = [0,20]
dt = 0.05
t = np.arange(t_span[0], t_span[1], dt)

# 初期件
th1 = 60.0
w1 = 0.0
th2 = -10.0
w2 = 0.0
state = np.radians([th1, w1, th2, w2])

# 運動方程式を解く
solved = solve_ivp(derivs, t_span, state, t_eval=t)
y = solved.y


# In[5]:


# ジェネレータ
def gen():
    for tt, th1, th2 in zip(t,y[0,:], y[2,:]):
        x1 = L1*sin(th1)
        y1 = -L1*cos(th1)
        x2 = L2*sin(th2) + x1
        y2 = -L2*cos(th2) + y1
        yield tt, x1, y1, x2, y2


# In[7]:


fig, ax = plt.subplots()
ax.set_title("DoublePendulumModel")
ax.set_xlim(-(L1+L2) - 0.3, L1+L2 + 0.3)
ax.set_ylim(-(L1+L2) - 0.3, L1+L2 + 0.3)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.minorticks_on()
ax.set_aspect('equal')
ax.grid()

locus, = ax.plot([], [], 'r-', linewidth=2, color="g")
line, = ax.plot([], [], 'o-', linewidth=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

ax.text(0.8, 1.3, "L1 = 1.0 m")
ax.text(0.8, 1.2, "L2 = 0.3 m")

ax.text(0.8, 1.0, "M1 = 2.5 kg")
ax.text(0.8, 0.9, "M2 = 0.3 kg")

xlocus, ylocus = [], []

def animate(data):
    t, x1, y1, x2, y2 = data
    xlocus.append(x2)
    ylocus.append(y2)

    locus.set_data(xlocus, ylocus)
    line.set_data([0, x1, x2], [0, y1, y2])
    time_text.set_text(time_template % (t))

ani = FuncAnimation(fig, animate, gen, interval=50, repeat=True)

plt.show()


# In[16]:


#ani.save('anim.gif', writer="pillow", fps=15)


# In[ ]:




