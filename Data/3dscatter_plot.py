# 3d scatter plot of ultrasonic data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import csv
from pathlib import Path
import os.path
import pseudotimedomain as ptd
import scipy.io as sio


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

px,py,pz = pseudo_signal.cartesianPeaks(peak_positions,0.15,-0.03,np.array([x/100 for x in radui]))

# save interpolated data to matlab file
pseudo_signal.findResponseAmplitude3D(0.15,-0.03,np.array([x/100 for x in radui]))
print("Interpolated data")
# save pseudo_signal.response_amplitude to matlab file
save_path = os.path.join(Path(__file__).resolve().parents[1], os.path.join("Data", "response_amplitude.mat"))
sio.savemat(save_path, {'response_amplitude': pseudo_signal.response_amplitude})

# plot the peaks 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i_radius, radius in enumerate(radui):
    for i_angle, angle in enumerate(angles):
        ax.scatter(px[i_radius][i_angle],py[i_radius][i_angle],pz[i_radius][i_angle],s=[x*100 for x in peak_heights[i_radius][i_angle]],cmap=cm.jet, norm=colors.LogNorm())
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
            
# plot the data
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for i_radius, radius in enumerate(radui):
#     for i_angle, angle in enumerate(angles):
#         ax.scatter(pseudo_signal.distance_x[:,i_radius,i_angle],pseudo_signal.distance_y[:,i_radius,i_angle],pseudo_signal.distance_z[:,i_radius,i_angle],c=pseudo_signal.distance_responses[:,i_radius,i_angle],s=100,cmap=cm.jet, norm=colors.LogNorm())
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()