import numpy as np
import PseudoTimeDomain as ptd
import os.path
import csv
from pathlib import Path
import signalresponses

# create a PseudoTimeDomain object
pseudo_signal = ptd.PseudoTimeDomain(15, 20)

pipe_radius = 150 * 1e-3
radui = [7.5]

gain_time = []
# load data
for sensor_radius in radui:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "scan_data_time_8.1.csv"))), newline='') as f:
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

pseudo_signal.positionPings2D(gain_time[0], int(max_gain_time + pseudo_signal.ping_duration / 2 + 10))

print("Ping positions found")

x = np.linspace(-0.25, 0.25, 51)
y = np.linspace(-0.25, 0.25, 51)
z = np.linspace(0.01, 0.5, 50)

responses = signalresponses.find_saft(x,y,z,radui[0]/100, sensor_angles, pseudo_signal.signal_responses, pseudo_signal.distance, True)

print("saft complete")

responses = signalresponses.convert_to_db(responses)

# plot the responses
to_plot_x = int(1*len(x)/2)
to_plot_y = int(1*len(y)/2)
to_plot_z = int(1*len(z)/2)

signalresponses.plot_slices(responses, x, y, z, to_plot_x, to_plot_y, to_plot_z)

signalresponses.plot_isosurface(responses, x, y, z, pipe_radius)