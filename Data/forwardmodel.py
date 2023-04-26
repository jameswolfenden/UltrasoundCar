import numpy as np
import signalresponses
import pseudotimedomain as ptd
import matplotlib.pyplot as plt


# Define simulation parameters
radius = 0.15  # radius of pipe in meters
length = 1.0  # length of pipe in meters
frequency = 40000.0  # ultrasound frequency in Hz
c = 343.0  # speed of sound in air in m/s
attenuation = 0.15 # Np/m, check this

# Define transducer parameters
transducer_radius = 0.075  # radius of transducer from centre of pipe in meters
transducer_angle = np.linspace(0, 2 * np.pi, 36, endpoint=False)  # angle of transducer from centre of pipe in radians
transducer_x = transducer_radius * -np.cos(transducer_angle)  # x coordinate of transducer in meters
transducer_y = transducer_radius * np.sin(transducer_angle)  # y coordinate of transducer in meters
transducer_z = 0.0  # z coordinate of transducer in meters

# Define points at the radius of the pipe
point_angle = np.linspace(0, 2 * np.pi, 100, endpoint=False)  # angle of point from centre of pipe in radians
#point_angle = [0.0]
point_x = radius * -np.cos(point_angle)  # x coordinate of point in meters
point_y = radius * np.sin(point_angle)  # y coordinate of point in meters
point_z = np.linspace(0, length, 200)  # z coordinate of point in meters

#point_x = [0.0]
#point_y = [0.0]
#point_z = [0.2]

# Create ultrasound pulse of 8 cycles and hann window
pulse_cycles = 8  # number of cycles in pulse
pulse_length = 1 / frequency * pulse_cycles  # length of pulse in seconds
pulse_samples = 25 * pulse_cycles  # number of samples in pulse
pulse_time = np.linspace(0, pulse_length, pulse_samples)  # time vector for pulse in seconds
pulse = np.sin(2 * np.pi * frequency * pulse_time)  # pulse
pulse = pulse * np.hanning(pulse_samples)  # hann window

# Create time vector for simulation
time_length = 2 * length / c *1.5  # length of time vector in seconds
sample_rate = 1 / (pulse_length / pulse_samples)  # sample rate in Hz
time_samples = int(time_length * sample_rate)  # number of samples in time vector
time = np.linspace(0, time_length, time_samples)  # time vector in seconds

# Create empty array to store data
data = np.zeros((len(time), len(transducer_angle)))
data2 = np.zeros((len(time), len(transducer_angle)))

level = np.zeros((len(transducer_angle),len(point_angle), len(point_z)))

# Loop through transducer locations
for i in range(len(transducer_angle)):
    # Loop through point locations
    for j in range(len(point_angle)):
        for k in range(len(point_z)):
            # Calculate distance from transducer to point
            distance = np.sqrt((transducer_x[i] - point_x[j])**2 + (transducer_y[i] - point_y[j])**2 + (transducer_z - point_z[k])**2)
            # Calculate time for ultrasound pulse to travel from transducer to point and back
            time_delay = 2 * distance / c
            # Calculate time index for data
            time_index = np.argmin(np.abs(time - time_delay)) - int(pulse_samples / 2)
            time_index2 = np.argmin(np.abs(time - time_delay))
            # Calculate angle from transducer to point
            angle = np.arccos(np.abs(transducer_z - point_z[k]) / distance)
            # sinc function to model transducer
            sinc = np.sin(np.pi*0.0088/0.008575*np.sin(angle))/(np.pi*0.0088/0.008575*np.sin(angle))
            # Account for attenuation
            attenuation_scale = np.exp(-attenuation * distance * 2)
            # Account for beam spreading
            power_scale = 1/(distance * 2)
            if sinc < 0:
                sinc = 0
            # Add pulse to data
            data[time_index:time_index + pulse_samples,i] = data[time_index:time_index + pulse_samples,i] + pulse*sinc*attenuation_scale*power_scale
            data2[time_index:time_index + pulse_samples,i] = data2[time_index:time_index + pulse_samples,i] + 1*sinc*attenuation_scale*power_scale
            level[i,j,k] = sinc*attenuation_scale*power_scale

# plot level[0,:,:] using imshow
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(level[0,:,:], cmap='gray', aspect='auto')
ax.set_ylabel('Angle (rad)')
ax.set_xlabel('Depth (m)')
ax.set_title('Level')
plt.show()


# save data to csv file
#np.savetxt('data.csv', data, delimiter=',')

# simulate srf10
# 16 threshold levels
analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]
threshold_multiplier = 1 # to account for the fact that the signal amplitude is arbitrary so we need to scale it
threshold_addition = 0
threshold_levels = [1/x*40*threshold_multiplier+threshold_addition for x in analogue_gains]



# find position of first threshold crossing for each threshold level
threshold_crossings = np.zeros((len(transducer_angle), len(threshold_levels)), dtype=np.int32)
for i, threshold_level in enumerate(threshold_levels):
    threshold_crossings[:,i] = np.argmax(data/np.max(data) > threshold_level, axis=0)

print('Threshold crossings: ', threshold_crossings)

# plot the time domain response and the threshold crossings on the same plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot((data[:,0]))
ax.plot(threshold_crossings[0,:], (data[threshold_crossings[0,:],0]), 'o')
# plot line from x axis to threshold crossing
for i, threshold_crossing in enumerate(threshold_crossings[0,:]):
    ax.plot([threshold_crossing, threshold_crossing], [0, (data[threshold_crossing,0])], 'k-')
    # plot line from y axis to threshold crossing
    ax.plot([0, threshold_crossing], [(data[threshold_crossing,0]), (data[threshold_crossing,0])], 'k-')
ax.set_xlabel('Time')
ax.set_ylabel('Signal strength')
#plt.show()

# plot data2
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot((data2[:,0]))
ax.set_xlabel('Time')
ax.set_ylabel('Signal strength')
plt.show()


pseudo_signal = ptd.PseudoTimeDomain(8, 20)
pseudo_signal.positionPings2D(threshold_crossings, time_length*1e6)


# Create grid for plotting
x = np.linspace(-0.16, 0.16, 33)
y = np.linspace(-0.16, 0.16, 33)
z = np.linspace(0.01, 0.9, 90)

sensor_radii = [transducer_radius*100]
signal_responses_data = [data]

timestep = 1/sample_rate
print("timestep: ", timestep)
time_data = np.arange(0, data.shape[0]*timestep, timestep)
# convert time to distance
time_data = time_data*343/2

srf_sim = False
real_data = True

if real_data:
    responses = signalresponses.find_saft(x,y,z,[x/100 for x in sensor_radii], np.rad2deg(transducer_angle), signal_responses_data, time_data, False)
    responses = signalresponses.convert_to_db(responses)
    # plot the responses
    to_plot_x = int(1*len(x)/2)
    to_plot_y = int(1*len(y)/2)
    to_plot_z = int(1*len(z)/2)
    signalresponses.plot_slices(responses, x, y, z, to_plot_x, to_plot_y, to_plot_z)
    signalresponses.plot_isosurface(responses, x, y, z, radius)

if srf_sim:
    # srf10 simulation
    responses = signalresponses.find_saft(x,y,z,[x/100 for x in sensor_radii], np.rad2deg(transducer_angle), np.expand_dims(pseudo_signal.signal_responses, axis=0), pseudo_signal.distance, True)
    responses = signalresponses.convert_to_db(responses)
    # plot the responses
    to_plot_x = int(1*len(x)/2)
    to_plot_y = int(1*len(y)/2)
    to_plot_z = int(1*len(z)/2)
    signalresponses.plot_slices(responses, x, y, z, to_plot_x, to_plot_y, to_plot_z)
    signalresponses.plot_isosurface(responses, x, y, z, radius)
