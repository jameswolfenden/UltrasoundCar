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
#scan_distances = [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100, 112.5, 125, 137.5, 150, 162.5, 175]
scan_distances = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195]

gain_time = []
# load data
for distance in scan_distances:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", os.path.join("fullpipe2-2", "scan_"+str(distance*10)+".csv")))), newline='') as f:
        reader = csv.reader(f)
        gain_time_temp = list(reader)
    gain_time_2d = []
    for angle in gain_time_temp:
        gain_time_2d.append(
            [int(i.replace('[', '').replace(']', '')) for i in angle])
    gain_time.append(gain_time_2d)

# reduce scan_distances by i*1 each
#for i, distance in enumerate(scan_distances):
#    scan_distances[i] = distance - i*2

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


x = np.linspace(-0.16, 0.16, 25)
y = np.linspace(-0.16, 0.16, 25)
z = np.linspace(0.01, 0.30, 30)
d_z = z[1]-z[0]

responses = np.zeros((len(scan_distances), len(x), len(y), len(z)), dtype=np.complex128)
for i in range(len(scan_distances)):
    responses[i] = signalresponses.find_saft(x,y,z,[x/100 for x in sensor_radii], sensor_angles, np.expand_dims(responses_3d[i], axis=0), pseudo_signal.distance, True)


# combine the responses into one 3d array using the scan_distances as the z axis
z_offsets = [i/100 for i in scan_distances]
z_offets_indexes = [int(i/d_z) for i in z_offsets]
z_max = z_offsets[-1] + z[-1]
z_max_index = len(z) + z_offets_indexes[-1]
responses_combined = np.zeros((len(x), len(y), z_max_index), dtype=np.float64)
for i in range(len(scan_distances)):
    responses_combined[:, :, z_offets_indexes[i]:z_offets_indexes[i]+len(z)] += np.abs(responses[i])
z_ignore = 0.15
responses_combined[:, :, :int(z_ignore/d_z)] = 0

responses_combined = signalresponses.convert_to_db(responses_combined)

print("saft complete")

z_new = np.linspace(z[0], z_max, z_max_index)

signalresponses.plot_isosurface(responses_combined, x, y, z_new, pipe_radius, -8, True)

to_plot_x = int(1*len(x)/2)
to_plot_y = int(1*len(y)/2)
to_plot_z = int(1*len(z_new)/2)
signalresponses.plot_slices(responses_combined, x, y, z_new, to_plot_x, to_plot_y, to_plot_z)