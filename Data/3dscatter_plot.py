# 3d scatter plot of ultrasonic data
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

gain_time = []
# load data
for radius in range(0,16,3):
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "scan_data_"+str(radius)+".csv"))), newline='') as f:
        reader = csv.reader(f)
        gain_time_temp = list(reader)
    gain_time_2d = []
    for angle in gain_time_temp:
        gain_time_2d.append([int(i.replace('[','').replace(']','')) for i in angle])
    gain_time.append(gain_time_2d)

# constants
# Set the parameters for signal
frequency = 0.04
cycles = 15
points_per_cycle = 20
ping_duration = cycles/frequency
sample_frequency = frequency*points_per_cycle
signal_duration = 2000  # change this to 6000 ish for the full signal
distance_time_scale = 1/sample_frequency*343*10**-6/2  # 343m/s is the speed of sound and 10**6 is to convert to microseconds and 2 is to get the distance to the object
analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]

# create 3d array to store signal for each angle
signal_responses = np.zeros((int(signal_duration*sample_frequency),len(gain_time),len(gain_time[0])),dtype=complex)

# calculate the response at each distance for each angle
ifft_result = ifft([0,points_per_cycle,0], points_per_cycle)
signal_result = np.tile(ifft_result,cycles)
t = np.arange(cycles*points_per_cycle)
window = signal.windows.hann(cycles*points_per_cycle)
ping_shape = np.multiply(window,signal_result)
for i_radius, radius in enumerate(gain_time):
    for i_angle, angle in enumerate(radius):
        for i_ping, ping in enumerate(angle):
            if not (ping == 0 or ping >signal_duration-ping_duration/2): # make sure response is within the signal duration
                signal_responses[int(ping*sample_frequency)-math.ceil(cycles*points_per_cycle/2):int(ping*sample_frequency)+int(cycles*points_per_cycle/2),i_radius,i_angle] +=ping_shape*1/math.sqrt(analogue_gains[i_ping])
distance_responses = np.abs(signal_responses)
distance_responses[ distance_responses==0 ] = np.nan # set 0 values to nan so they are not plotted

# convert angle and radius to x and y
x = np.zeros((len(gain_time),len(gain_time[0])))
z = np.zeros((len(gain_time),len(gain_time[0])))
y = 0.15 # scan being taken 20cm from sensor
angles = np.arange(0,360, int(360/len(gain_time[0])))
radui = np.arange(0,0.16,0.03)
for i_radius, radius in enumerate(radui):
    for i_angle, angle in enumerate(angles):
        z[i_radius,i_angle] = -math.cos(math.radians(angle))*radius # minus sign is for starting at the bottom
        x[i_radius,i_angle] = math.sin(math.radians(angle))*radius
modulus = np.sqrt(x**2+y**2+z**2)
x = np.multiply(x,1/modulus)
y = np.multiply(y,1/modulus)
z = np.multiply(z,1/modulus)

distance = np.arange(0,(int(signal_duration*sample_frequency))*distance_time_scale,distance_time_scale)

# create a 3d array to store the distance in x,y,z for each angle and radius
distance_x = np.zeros((len(distance),len(gain_time),len(gain_time[0])))
distance_y = np.zeros((len(distance),len(gain_time),len(gain_time[0])))
distance_z = np.zeros((len(distance),len(gain_time),len(gain_time[0])))
for i_radius, radius in enumerate(radui):
    for i_angle, angle in enumerate(angles):
        distance_x[:,i_radius,i_angle] = distance*x[i_radius,i_angle]
        distance_y[:,i_radius,i_angle] = distance*y[i_radius,i_angle]
        distance_z[:,i_radius,i_angle] = distance*z[i_radius,i_angle]


# plot the data
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i_radius, radius in enumerate(radui):
    for i_angle, angle in enumerate(angles):
        ax.scatter(distance_x[:,i_radius,i_angle],distance_y[:,i_radius,i_angle],distance_z[:,i_radius,i_angle],c=distance_responses[:,i_radius,i_angle],s=100,cmap=cm.jet, norm=colors.LogNorm())
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()