# plot a graph showing the peak amplitude of the pseudotimedomain signals
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import csv
from pathlib import Path
import os.path
import pseudotimedomain as ptd
from scipy.interpolate import griddata
import math


radui = range(5,16,5)

gain_time = []
# load data
for radius in radui:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "radius_"+str(radius)+".csv"))), newline='') as f:
        reader = csv.reader(f)
        gain_time_temp = list(reader)
    gain_time_2d = []
    for angle in gain_time_temp:
        gain_time_2d.append([int(i.replace('[','').replace(']','')) for i in angle])
    gain_time.append(gain_time_2d)

angles = np.arange(0,360, int(360/len(gain_time[0])))

pseudo_signal = ptd.PseudoTimeDomain(15,20)
pseudo_signal.positionPings3D(gain_time,6000)
pseudo_signal.sphericalToCartesian(0.15,-0.03,np.array([x/100 for x in radui]))

peak_heights, peak_positions = pseudo_signal.findPeaks3D(pseudo_signal.distance_responses)
# find the highest peak for each radius and angle
peaks = []
for peak_radius in peak_heights:
    peaks.append([])
    for peak_angle in peak_radius:
        if len(peak_angle) == 0:
            peaks[-1].append(0)
        else:
            peaks[-1].append(max(peak_angle))
# convert to numpy array
peaks = np.array(peaks)

# flatten peaks array
peaks_flat = peaks.flatten()
# convert angles and radius to x and y columns
radui_flat = np.array([x for x in radui for y in angles])
angles_flat = np.array([y for x in radui for y in angles])
x = -radui_flat*np.sin(np.radians(angles_flat))
y = -radui_flat*np.cos(np.radians(angles_flat))

# interpolate the data
xi = np.linspace(min(x),max(x),100)
yi = np.linspace(min(y),max(y),100)
zi = griddata((x,y),peaks_flat,(xi[None,:],yi[:,None]),method='cubic')

# replace nan values with 0 in zi
zi = np.nan_to_num(zi)

# plot the data in 2d using imshow
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(zi, aspect='auto', extent=[min(x),max(x),min(y),max(y)], cmap='jet')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_title("Peak Amplitude of PseudoTimeDomain Signals")
fig.colorbar(ax.imshow(zi, aspect='auto', extent=[min(x),max(x),min(y),max(y)], cmap='jet'), ax=ax)

# plot the uninterpolated data in polar coordinates
fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
c = ax.pcolormesh(np.radians(angles), radui, peaks, cmap='jet')
ax.set_theta_zero_location("N")
ax.set_theta_direction(1)
ax.set_rlabel_position(0)
ax.set_rmax(15)
ax.set_rticks([5,10,15])
ax.set_rlabel_position(90)
ax.set_title("Peak Amplitude of PseudoTimeDomain Signals", va='bottom')
ax.set_xlabel('Radius (m)')
ax.set_ylabel('Angle (degrees)')
fig.colorbar(c, ax=ax)

plt.show()