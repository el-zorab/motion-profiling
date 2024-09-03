import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np
import math

fig, ax = plt.subplots()

fig.set_figwidth(8)
fig.set_figheight(5)

fig.subplots_adjust(bottom=0.3)

vel_max   = 2
accel_max = 1.5
decel_max = 1.0
distance = 12

# Sliders

vel_max_axes = fig.add_axes([0.25, 0.17, 0.55, 0.03])
vel_max_slider = Slider(
    ax=vel_max_axes,
    label='Max Velocity',
    valmin=0.05,
    valmax=5,
    valinit=vel_max
)

accel_max_axes = fig.add_axes([0.25, 0.12, 0.55, 0.03])
accel_max_slider = Slider(
    ax=accel_max_axes,
    label='Max Acceleration',
    valmin=0.05,
    valmax=5,
    valinit=accel_max
)

decel_max_axes = fig.add_axes([0.25, 0.07, 0.55, 0.03])
decel_max_slider = Slider(
    ax=decel_max_axes,
    label='Max Deceleration',
    valmin=0.05,
    valmax=5,
    valinit=decel_max
)

distance_axes = fig.add_axes([0.25, 0.02, 0.55, 0.03])
distance_slider = Slider(
    ax=distance_axes,
    label='Distance',
    valmin=0.1,
    valmax=15,
    valinit=distance
)

accel_dx = 0
cruise_dx = 0
decel_dx = 0

accel_dt = 0
cruise_dt = 0
decel_dt = 0

def accel_func(time):
    return 0.5 * accel_max * time ** 2

def cruise_func(time):
    return accel_dx + vel_max * (time - accel_dt)

def decel_func(time):
    return accel_dx + cruise_dx + vel_max * (time - accel_dt - cruise_dt) - 0.5 * decel_max * (time - accel_dt - cruise_dt) ** 2

def render(unused):
    global vel_max, accel_max, decel_max, distance
    vel_max   = vel_max_slider.val
    accel_max = accel_max_slider.val
    decel_max = decel_max_slider.val
    distance = distance_slider.val

    global accel_dx, cruise_dx, decel_dx, accel_dt, cruise_dt, decel_dt

    vel_max_limit = math.sqrt((2 * distance * accel_max * decel_max) / (accel_max + decel_max))
    if (vel_max > vel_max_limit):
        vel_max = vel_max_limit

    accel_dt = vel_max / accel_max
    accel_dx = 0.5 * accel_max * accel_dt ** 2

    decel_dt = vel_max / decel_max
    decel_dx = vel_max * decel_dt - 0.5 * decel_max * decel_dt ** 2

    cruise_dx = distance - accel_dx - decel_dx
    cruise_dt = cruise_dx / vel_max

    accel_time_vals = np.linspace(0, accel_dt, 100)
    accel_func_vals = list(map(accel_func, accel_time_vals))

    cruise_time_vals = np.linspace(accel_dt, accel_dt + cruise_dt, 100)
    cruise_func_vals = list(map(cruise_func, cruise_time_vals))

    decel_time_vals = np.linspace(accel_dt + cruise_dt, accel_dt + cruise_dt + decel_dt, 100)
    decel_func_vals = list(map(decel_func, decel_time_vals))

    ax.clear()
    ax.set_title("Motion Profile")
    ax.set_xlabel("Time")
    ax.set_ylabel("Distance")
    ax.set_xlim([0, 15])
    ax.set_ylim([0, 15])

    ax.hlines(y = accel_dx,                        xmin = 0.0, xmax = accel_dt,                        color = 'k', linestyle = 'dashed')
    ax.hlines(y = accel_dx + cruise_dx,            xmin = 0.0, xmax = accel_dt + cruise_dt,            color = 'k', linestyle = 'dashed')
    ax.hlines(y = accel_dx + cruise_dx + decel_dx, xmin = 0.0, xmax = accel_dt + cruise_dt + decel_dt, color = 'k', linestyle = 'dashed')
    
    ax.plot(accel_time_vals, accel_func_vals)
    ax.plot(cruise_time_vals, cruise_func_vals)
    ax.plot(decel_time_vals, decel_func_vals)

vel_max_slider.on_changed(render)
accel_max_slider.on_changed(render)
decel_max_slider.on_changed(render)
distance_slider.on_changed(render)

render(0)

plt.show()
