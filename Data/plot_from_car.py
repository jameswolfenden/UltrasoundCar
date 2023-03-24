import numpy as np
import PseudoTimeDomain as ptd
import os.path
import csv
from pathlib import Path
import signalresponses

# create a PseudoTimeDomain object
pseudo_signal = ptd.PseudoTimeDomain(8, 20)

pipe_radius = 150 * 1e-3
sensor_radii = [7.5]

gain_time = []
# load data
for sensor_radius in sensor_radii:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", os.path.join("tjunct", "scan_data_time_7.5.csv")))), newline='') as f:
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

responses_3d = np.zeros((len(sensor_radii), int(int(max_gain_time + pseudo_signal.ping_duration / 2 + 10)*pseudo_signal.sample_frequency), len(sensor_angles)), dtype=np.complex128)
for i, sensor_radius in enumerate(sensor_radii):
    pseudo_signal.positionPings2D(gain_time[i], int(max_gain_time + pseudo_signal.ping_duration / 2 + 10))
    responses_3d[i] = pseudo_signal.signal_responses

print("Ping positions found")

x = np.linspace(-0.17, 0.17, 51)
y = np.linspace(-0.17, 0.17, 51)
z = np.linspace(0.01, 0.75, 50)

responses = signalresponses.find_saft(x,y,z,[x/100 for x in sensor_radii], sensor_angles, responses_3d, pseudo_signal.distance, True)

print("saft complete")

responses = signalresponses.convert_to_db(responses)

# plot the responses
to_plot_x = int(1*len(x)/2)
to_plot_y = int(1*len(y)/2)
to_plot_z = int(1*len(z)/2)

signalresponses.plot_slices(responses, x, y, z, to_plot_x, to_plot_y, to_plot_z)

signalresponses.plot_isosurface(responses, x, y, z, pipe_radius)