import pseudotimedomain as ptd
import numpy as np
import matplotlib.pyplot as plt
import csv
from pathlib import Path
import os.path

distances = np.arange(5, 101, 5)
gain_time_full = []
for dist in distances:
    # Read in the csv into a 2d array with each row being a ping at a different angle and each column being a different gain
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", os.path.join("attenuation", "attenuation_data"+str(dist)+".csv")))), newline='') as f:
        reader = csv.reader(f)
        gain_time = list(reader)
    # Convert the string 2d array to a int 2d array
    gain_time = [int(i.replace('[','').replace(']','')) for i in gain_time[0]]
    gain_time_full.append(gain_time)

pseudo_signal = ptd.PseudoTimeDomain(8,20)
pseudo_signal.positionPings2D(gain_time_full,6000)

peak_heights, peak_positions = pseudo_signal.findPeaks2D(pseudo_signal.distance_responses)

# Plot the distance responses
plt.figure()
plt.imshow(pseudo_signal.distance_responses, vmin=0, vmax=np.max(np.abs(pseudo_signal.distance_responses)), aspect='auto', extent=[0,360,pseudo_signal.distance_responses.shape[0]*pseudo_signal.distance_time_scale,0], cmap='jet')
#for i in range(len(peak_heights)):
#    plt.plot([i*180/8-80 for x in peak_positions[i]],[b*pseudo_signal.distance_time_scale for b in peak_positions[i]],  'ro')
plt.xlabel('Angle (degrees)')
plt.ylabel('Distance (m)')
plt.show()

# plot the first distance response against distance
plt.figure()
plt.plot(pseudo_signal.distance, pseudo_signal.distance_responses)
plt.xlabel('Distance (m)')
plt.ylabel('Signal strength')
plt.show()
