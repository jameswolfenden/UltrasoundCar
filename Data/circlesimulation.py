# simulate the ray tracing of ultrasound around a 2d circle from the transducer back to the receiver
import numpy as np
import matplotlib.pyplot as plt

# define the transducer and receiver
transducer_radius = 0.00970/2  # radius of transducer
receiver_radius = 0.00970/2  # radius of receiver
transducer_to_receiver = 0.01778  # distance from transducer to receiver
sensor_position = [0.0, 0.075]  # position of the sensor
# find transducer and receiver centres
transducer_centre = [sensor_position[0] - transducer_to_receiver/2, sensor_position[1]]
receiver_centre = [sensor_position[0] + transducer_to_receiver/2, sensor_position[1]]

# define the radius of the circle
pipe_radius = 0.15

# define the number of rays to simulate
num_rays = 1000

# define the speed of sound
speed_of_sound = 343

# define frequency of ultrasound
frequency = 40000

# Create ultrasound pulse of 8 cycles and hann window
pulse_cycles = 8  # number of cycles in pulse
pulse_length = 1 / frequency * pulse_cycles  # length of pulse in seconds
samples_per_cycle = 25
pulse_samples = samples_per_cycle * pulse_cycles  # number of samples in pulse
pulse_time = np.linspace(0, pulse_length, pulse_samples)  # time vector for pulse in seconds
pulse = np.sin(2 * np.pi * frequency * pulse_time)  # pulse
pulse = pulse * np.hanning(pulse_samples)  # hann window

# define time to simulate
max_time = 30 * pipe_radius / speed_of_sound

# define the time step
time_step = 1 / (samples_per_cycle * frequency)

# define the number of samples
num_samples = int(max_time / time_step)

# define array to store the data at the receiver for each ray
data = np.zeros((num_rays, num_samples))

# define the angles of the rays
angles = np.linspace(0, 2 * np.pi, num_rays, endpoint=False)

# define starting point of the rays
x = transducer_radius * np.cos(angles) + transducer_centre[0]
y = transducer_radius * np.sin(angles) + transducer_centre[1]

# define starting times
t = np.zeros(num_rays)

# define the number of reflections
num_reflections = 16
for reflection in range(num_reflections):

    # find the intersection of the rays with the pipe wall
    # define the equation of the line for each ray
    m = np.tan(angles)
    slope = y - m * x

    # find the intersection of the line with the circle
    # define the quadratic equation
    a = 1 + m ** 2
    b = 2 * m * slope
    c = slope ** 2 - pipe_radius ** 2

    # find the roots of the quadratic equation
    x1 = (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x2 = (-b - np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)

    # find the correct root
    x_new = np.zeros(num_rays)
    y_new = np.zeros(num_rays)
    for i in range(num_rays):
        if angles[i] < np.pi / 2 or angles[i] > 3 * np.pi / 2:
            if x1[i] > x[i]:
                x_new[i] = x1[i]
                if angles[i] < np.pi / 2:
                    y_new[i] = np.sqrt(pipe_radius ** 2 - x_new[i] ** 2)
                else:
                    y_new[i] = -np.sqrt(pipe_radius ** 2 - x_new[i] ** 2)
            else:
                x_new[i] = x2[i]
                if angles[i] < np.pi / 2:
                    y_new[i] = np.sqrt(pipe_radius ** 2 - x_new[i] ** 2)
                else:
                    y_new[i] = -np.sqrt(pipe_radius ** 2 - x_new[i] ** 2)
        else:
            if x1[i] < x[i]:
                x_new[i] = x1[i]
                if angles[i] < np.pi / 2:
                    y_new[i] = np.sqrt(pipe_radius ** 2 - x_new[i] ** 2)
                else:
                    y_new[i] = -np.sqrt(pipe_radius ** 2 - x_new[i] ** 2)
            else:
                x_new[i] = x2[i]
                if angles[i] < np.pi / 2:
                    y_new[i] = np.sqrt(pipe_radius ** 2 - x_new[i] ** 2)
                else:
                    y_new[i] = -np.sqrt(pipe_radius ** 2 - x_new[i] ** 2)

    # find the distance travelled by each ray
    d = np.sqrt((x_new - x) ** 2 + (y_new - y) ** 2)

    # find the time taken by each ray
    t_new = d / speed_of_sound

    # find the angle from the centre of the circle to the point of intersection
    theta = np.arctan2(y_new, x_new)

    # find the angle change of the rays after reflection
    angles_change = 2 * (theta - angles)

    # find the angle of the reflected rays
    angles_new = np.pi - angles + angles_change

    # make sure the angles are between 0 and 2pi
    angles_new = np.mod(angles_new, 2 * np.pi)

    # find the rays that hit the receiver and the time taken
    # define the equation of the line for each ray
    m = np.tan(angles)
    slope = y - m * x

    # define the equation of the circle for the receiver
    a = 1 + m ** 2
    b = 2 * m * slope - 2 * receiver_centre[0] - 2 * receiver_centre[1] * m
    c = slope ** 2 - 2 * receiver_centre[1] * slope + receiver_centre[0] ** 2 + receiver_centre[1] ** 2 - receiver_radius ** 2

    # find the roots of the quadratic equation
    x1_hit = (-b + np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x2_hit = (-b - np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)

    # find the correct root
    x_hit = np.zeros(num_rays)
    y_hit = np.zeros(num_rays)
    hit = np.full(num_rays, False)
    # ensure the ray is travelling towards the receiver
    for i in range(num_rays):
        if angles[i] < np.pi / 2 or angles[i] > 3 * np.pi / 2:
            if x1_hit[i] > x[i] or x2_hit[i] > x[i]:
                hit[i] = True
                # get the closest root
                if x1_hit[i] < x2_hit[i]:
                    x_hit[i] = x1_hit[i]
                    y_hit[i] = x_hit[i] * m[i] + slope[i]
                else:
                    x_hit[i] = x2_hit[i]
                    y_hit[i] = x_hit[i] * m[i] + slope[i]
        else:
            if x1_hit[i] < x[i] or x2_hit[i] < x[i]:
                hit[i] = True
                # get the closest root
                if x1_hit[i] > x2_hit[i]:
                    x_hit[i] = x1_hit[i]
                    y_hit[i] = x_hit[i] * m[i] + slope[i]
                else:
                    x_hit[i] = x2_hit[i]
                    y_hit[i] = x_hit[i] * m[i] + slope[i]
        # check to see if y hit is nan
        if np.isnan(y_hit[i]):
            hit[i] = False
            x_hit[i] = 0

    # find the distance travelled by each ray
    d_hit = np.sqrt((x_hit[hit] - x[hit]) ** 2 + (y_hit[hit] - x[hit]) ** 2)

    # find the time taken by each ray
    t_hit = d_hit / speed_of_sound + t[hit]

    # find the index of the time taken
    index = np.round(t_hit / time_step).astype(int)

    # hit index
    hit_index = np.where(hit)[0]

    # find the data at the receiver
    for i in range(len(hit_index)):
        test = data[hit_index[i], index[i]:index[i] + pulse_samples] 
        data[hit_index[i], index[i]:index[i] + pulse_samples] += pulse

    x = x_new
    y = y_new
    angles = angles_new
    t += t_new

# sum the data
data_sum = np.sum(data, axis=0)
# plot the data
plt.figure()
plt.plot(np.linspace(0, max_time, len(data_sum)), data_sum)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Data at Receiver')
plt.show()

# visualize the pipe, transducer and receiver and the rays
# define the circle for the pipe
theta = np.linspace(0, 2 * np.pi, 100)
x_circle = pipe_radius * np.cos(theta)
y_circle = pipe_radius * np.sin(theta)

# define the circle for the transducer
theta = np.linspace(0, 2 * np.pi, 100)
x_transducer = transducer_radius * np.cos(theta) + transducer_centre[0]
y_transducer = transducer_radius * np.sin(theta) + transducer_centre[1]

# define the circle for the receiver
theta = np.linspace(0, 2 * np.pi, 100)
x_receiver = receiver_radius * np.cos(theta) + receiver_centre[0]
y_receiver = receiver_radius * np.sin(theta) + receiver_centre[1]

# plot the pipe, transducer and receiver and the rays start and end points
plt.figure()
plt.plot(x_circle, y_circle, 'k')
plt.plot(x_transducer, y_transducer, 'k')
plt.plot(x_receiver, y_receiver, 'k')
plt.plot(x, y, 'r.')
plt.plot(x_hit[hit], y_hit[hit], 'b.')
# draw lines from hits to start points
for i in range(len(hit_index)):
    plt.plot([x[hit_index[i]], x_hit[hit][i]], [y[hit_index[i]], y_hit[hit][i]], 'g')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Pipe, Transducer, Receiver and Rays')
plt.show()

# plot the data
#plt.figure()
#plt.imshow(data, aspect='auto', extent=[0, max_time, 0, num_rays])
#plt.xlabel('Time (s)')
#plt.ylabel('Ray')
#plt.title('Data at Receiver')
#plt.show()

