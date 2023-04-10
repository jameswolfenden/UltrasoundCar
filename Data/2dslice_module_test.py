import PseudoTimeDomain as ptd
import numpy as np
import matplotlib.pyplot as plt
import csv
from pathlib import Path
import os.path

sensor_radius = 7.5

# Read in the csv into a 2d array with each row being a ping at a different angle and each column being a different gain
with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", os.path.join("block1-20", "scan_data_time_"+str(sensor_radius)+".csv")))), newline='') as f:
    reader = csv.reader(f)
    gain_time = list(reader)
# Convert the string 2d array to a int 2d array
for i, row in enumerate(gain_time):
    gain_time[i] = [int(i.replace('[','').replace(']','')) for i in row]

pseudo_signal = ptd.PseudoTimeDomain(8,20)
pseudo_signal.positionPings2D(gain_time,6000)

peak_heights, peak_positions = pseudo_signal.findPeaks2D(pseudo_signal.distance_responses)

# get the distance responses mapped to the correct angle (only works for 36 scans soz)
distance_responses = np.zeros_like(pseudo_signal.distance_responses)
distance_responses[:,0:27] = pseudo_signal.distance_responses[:,9:36]
distance_responses[:,27:36] = pseudo_signal.distance_responses[:,0:9]

# Plot the distance responses
plt.figure()
plt.imshow(distance_responses, vmin=0, vmax=np.max(np.abs(distance_responses)), aspect='auto', extent=[0,360,distance_responses.shape[0]*pseudo_signal.distance_time_scale,0], cmap='jet')
#for i in range(len(peak_heights)):
#    plt.plot([i*180/8-80 for x in peak_positions[i]],[b*pseudo_signal.distance_time_scale for b in peak_positions[i]],  'ro')
plt.xlabel('Angle (degrees)')
plt.ylabel('Distance (m)')
plt.show()

# plot the first distance response against distance
plt.figure()
plt.plot(pseudo_signal.distance, pseudo_signal.signal_responses[:,27])
plt.xlabel('Distance (m)')
plt.ylabel('Signal strength')
plt.show()
