import numpy as np
import pseudotimedomain as ptd
import os.path
import csv
from pathlib import Path
import signalresponses
import matplotlib.pyplot as plt

# create a PseudoTimeDomain object
pseudo_signal = ptd.PseudoTimeDomain(8, 20)

pipe_radius = 150 * 1e-3
sensor_radii = [7.5]
scan_distances = [0, 20, 40]

gain_time = []
# load data
for distance in scan_distances:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", os.path.join("distance_scan", "scan_"+str(distance)+".csv")))), newline='') as f:
        reader = csv.reader(f)
        gain_time_temp = list(reader)
    gain_time_2d = []
    for angle in gain_time_temp:
        gain_time_2d.append(
            [int(i.replace('[', '').replace(']', '')) for i in angle])
    gain_time.append(gain_time_2d)

sensor_angles = np.arange(0, 360, int(360/len(gain_time[0])))-90  # start at 9 o'clock

# use the pseudo time domain object to find the responses using the gain time data
# important the [0]!!!!!!!!!!
# find largest value in gain_time[0]
max_gain_time = max([max(i) for i in gain_time[0]])
if max_gain_time<5000:
    max_gain_time = 5000

responses_3d = np.zeros((len(scan_distances), int(int(max_gain_time + pseudo_signal.ping_duration / 2 + 10)*pseudo_signal.sample_frequency), len(sensor_angles)), dtype=np.complex128)
for i, distance in enumerate(scan_distances):
    pseudo_signal.positionPings2D(gain_time[i], int(max_gain_time + pseudo_signal.ping_duration / 2 + 10))
    responses_3d[i] = pseudo_signal.signal_responses

print("Ping positions found")

# plot the first response against distance
plt.figure()
for i in range(len(scan_distances)):
    plt.plot(pseudo_signal.distance, pseudo_signal.signal_responses[:, :].real)
    plt.plot(pseudo_signal.distance, pseudo_signal.signal_responses[:, :].imag)
    plt.plot(pseudo_signal.distance, np.abs(pseudo_signal.signal_responses[:, :]))
plt.xlabel('Distance (m)')
plt.ylabel('Signal strength')
plt.show()

x = np.linspace(-0.17, 0.17, 51)
y = np.linspace(-0.17, 0.17, 51)
z = np.linspace(0.01, 0.70, 70)
d_z = z[1]-z[0]

responses = np.zeros((len(scan_distances), len(x), len(y), len(z)), dtype=np.complex128)
for i in range(len(scan_distances)):
    responses[i] = signalresponses.find_saft(x,y,z,[x/100 for x in sensor_radii], sensor_angles, np.expand_dims(responses_3d[i], axis=0), pseudo_signal.distance, True)


plt.figure()
plt.plot(responses[0, 25, 25, :].real)
plt.plot(responses[0, 25, 25, :].imag)
plt.plot(np.abs(responses[0, 25, 25, :]))
plt.show()

# combine the responses into one 3d array using the scan_distances as the z axis
z_offsets = [i/100 for i in scan_distances]
z_offets_indexes = [int(i/d_z) for i in z_offsets]
z_max = z_offsets[-1] + z[-1]
z_max_index = int(z_max/d_z)
responses_combined = np.zeros((len(x), len(y), z_max_index), dtype=np.float64)
for i in range(len(scan_distances)):
    responses_combined[:, :, z_offets_indexes[i]:z_offets_indexes[i]+len(z)] += np.abs(responses[i])

responses_combined = signalresponses.convert_to_db(responses_combined, 4*3)

print("saft complete")

z_new = np.linspace(z[0], z_max, z_max_index)

signalresponses.plot_isosurface(responses_combined, x, y, z_new, pipe_radius)