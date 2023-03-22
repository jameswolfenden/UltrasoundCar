import numpy as np
import os.path
import signalresponses
import pandas as pd


pipe_radius = 150 * 1e-3
sensor_radius = 7.5e-2

# Read in the data using pandas
signal_responses_data = pd.read_csv(os.path.join("Data","radiustimedata7.5.csv"), header=None).to_numpy()
timestep = 2.5*1e-6 # change!!!!!
print("timestep: ", timestep)

signal_responses_data = np.append(signal_responses_data, np.zeros((100,len(signal_responses_data[0]))), axis=0)

time_data = np.arange(0, len(signal_responses_data[:,0]))*timestep
# convert time to distance
time_data = time_data*343/2

sensor_angles = np.arange(0, 360, int(360/len(signal_responses_data[0])))-90  # start at 9 o'clock

print("Ping positions found")

x = np.linspace(-0.20, 0.20, 51)
y = np.linspace(-0.20, 0.20, 51)
z = np.linspace(0.01, 0.25, 50)

responses = signalresponses.find_saft(x,y,z,sensor_radius, sensor_angles, signal_responses_data, time_data, False)

print("saft complete")

responses = signalresponses.convert_to_db(responses)

# plot the responses
to_plot_x = int(1*len(x)/2)
to_plot_y = int(1*len(y)/2)
to_plot_z = int(1*len(z)/2)

signalresponses.plot_slices(responses, x, y, z, to_plot_x, to_plot_y, to_plot_z)

signalresponses.plot_isosurface(responses, x, y, z, pipe_radius)