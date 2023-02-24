# 3d scatter plot of ultrasonic data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import csv
from pathlib import Path
import os.path
import PseudoTimeDomain as ptd

radui = range(0,15,1)

gain_time = []
# load data
for radius in radui:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "scan_data_time_"+str(radius)+".csv"))), newline='') as f:
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

px,py,pz = pseudo_signal.cartesianPeaks(peak_positions,0.15,-0.03,np.array([x/100 for x in radui]))

#plot the peaks 
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for i_radius, radius in enumerate(radui):
#     for i_angle, angle in enumerate(angles):
#         ax.scatter(px[:,i_radius,i_angle],py[:,i_radius,i_angle],pz[:,i_radius,i_angle],c=pseudo_signal.distance_responses[:,i_radius,i_angle],s=100,cmap=cm.jet, norm=colors.LogNorm())
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()
            
# plot the data
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i_radius, radius in enumerate(radui):
    for i_angle, angle in enumerate(angles):
        ax.scatter(pseudo_signal.distance_x[:,i_radius,i_angle],pseudo_signal.distance_y[:,i_radius,i_angle],pseudo_signal.distance_z[:,i_radius,i_angle],c=pseudo_signal.distance_responses[:,i_radius,i_angle],s=100,cmap=cm.jet, norm=colors.LogNorm())
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()