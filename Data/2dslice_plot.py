# 2D slice plot
#
# import the necessary packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import math
import csv
from pathlib import Path
import os.path
import scipy.signal as signal
from scipy.fft import ifft
import scipy.io as sio

# Read in the csv into a 2d array with each row being a ping at a different angle and each column being a different gain
with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "gain_pings.csv"))), newline='') as f:
    reader = csv.reader(f)
    gain_time = list(reader)
# Convert the string 2d array to a int 2d array
for i, row in enumerate(gain_time):
    gain_time[i] = [int(i) for i in row]

print(gain_time)

# Set the parameters for signal
frequency = 0.04
cycles = 15
points_per_cycle = 20
ping_duration = cycles/frequency
sample_frequency = frequency*points_per_cycle
signal_duration = 2000  # change this to 6000 ish for the full signal
distance_time_scale = 1/sample_frequency*343*10**-6/2  # 343m/s is the speed of sound and 10**6 is to convert to microseconds and 2 is to get the distance to the object
analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]

# Create the 2d array to store the signal for each angle
signal_responses = np.zeros((int(signal_duration*sample_frequency),len(gain_time)),dtype=complex)

# Calculate the response at each distance for each angle
ifft_result = ifft([0,points_per_cycle,0], points_per_cycle)
signal_result = np.tile(ifft_result,cycles)
t = np.arange(cycles*points_per_cycle)
window = signal.windows.hann(cycles*points_per_cycle)
ping_shape = np.multiply(window,signal_result)
for i_angle, angle in enumerate(gain_time):
    for i_ping, ping in enumerate(angle):
        if not (ping == 0 or ping >signal_duration-ping_duration/2): # make sure response is within the signal duration
            signal_responses[int(ping*sample_frequency)-math.ceil(cycles*points_per_cycle/2):int(ping*sample_frequency)+int(cycles*points_per_cycle/2),i_angle] +=ping_shape*1/math.sqrt(analogue_gains[i_ping])

distance_responses = abs(signal_responses) # signal_responses is complex so take the absolute value

# Plot the distance responses
plt.figure()
plt.imshow(distance_responses, vmin=0, vmax=np.abs(distance_responses).max(), aspect='auto', extent=[-90,90,distance_responses.shape[0]*distance_time_scale,0], cmap='jet')
plt.xlabel('Angle (degrees)')
plt.ylabel('Distance (m)')
plt.show()