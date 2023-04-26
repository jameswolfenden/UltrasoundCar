import numpy as np
import os.path
import signalresponses
import pandas as pd
import matplotlib.pyplot as plt


pipe_radius = 20 * 1e-3
sensor_radii = [0.5]

timestep = 1e-6 # change!!!!!
min_time = 800e-6 

# Read in the data using pandas
signal_responses_read = pd.read_csv(os.path.join("Data","anglesgip.csv"), header=None).to_numpy()
# crop off the first 1000 rows
#signal_responses_read = signal_responses_read[50:, :]

print("timestep: ", timestep)

signal_responses_data = np.zeros((1, int(min_time/timestep), len(signal_responses_read[0])))

signal_responses_data[0, :signal_responses_read.shape[0], :signal_responses_read.shape[1]] = signal_responses_read

time_data = np.arange(0, int(min_time/timestep))*timestep
# convert time to distance
time_data = time_data*343/2

sensor_angles = np.arange(0, 360, int(360/len(signal_responses_data[0,0])))-90  # start at 9 o'clock - change to 80 if its offset because there must be an error in the data

# plot the signal responses data against angle
plt.figure()
plt.plot(sensor_angles, signal_responses_data[0, 0, :])
plt.xlabel("Angle (degrees)")
plt.ylabel("Signal response")
plt.title("Signal response against angle")
plt.show()

# plot the first signal response against distance
plt.figure()
plt.plot(time_data, signal_responses_data[0, :, 0])
plt.xlabel("Distance (m)")
plt.ylabel("Signal response")
plt.title("Signal response against distance")
plt.show()

print("Ping positions found")

x = np.linspace(-0.03, 0.03, 61)
y = np.linspace(-0.03, 0.03, 61)
z = np.linspace(0.02, 0.1, 99)

responses = signalresponses.find_saft(x,y,z,[x/100 for x in sensor_radii], sensor_angles, signal_responses_data, time_data, False)

print("saft complete")

responses = signalresponses.convert_to_db(responses)

# plot the responses
to_plot_x = int(1*len(x)/2)
to_plot_y = int(1*len(y)/2)
to_plot_z = int(1*len(z)/2)

signalresponses.plot_slices(responses, x, y, z, to_plot_x, to_plot_y, to_plot_z)

signalresponses.plot_isosurface(responses, x, y, z, pipe_radius)