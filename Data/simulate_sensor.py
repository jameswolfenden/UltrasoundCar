import numpy as np
from scipy.fft import ifft
import math
import matplotlib.pyplot as plt
import scipy.signal as signal
import PseudoTimeDomain as ptd



sample_frequency = 1e6
signal_length_seconds = 0.001
sin_frequency = 40e3
cycles = 8
points_per_cycle = int(sample_frequency/sin_frequency)

# create an array of zeros to store the time domain response
time_response = np.zeros(int(sample_frequency*signal_length_seconds), dtype=np.complex128)


ifft_result = ifft([0,points_per_cycle,0], points_per_cycle)
signal_result = np.tile(ifft_result,cycles)
window = signal.windows.hann(cycles*points_per_cycle)
signal_result = signal_result*window


signal_ping_position = np.arange(0.0002, signal_length_seconds, 0.0001)
# generate a random scale for each ping
signal_ping_scale = np.random.rand(len(signal_ping_position))
#signal_ping_position = [0.001, 0.002, 0.003, 0.004]
#signal_ping_scale = [0.25, 0.5, 0.75, 1]

for i, ping_position in enumerate(signal_ping_position):
    ping_position_samples = int(ping_position*sample_frequency)
    ping_position_samples_start = ping_position_samples - math.floor(cycles*points_per_cycle/2)
    ping_position_samples_end = ping_position_samples + math.ceil(cycles*points_per_cycle/2)
    time_response[ping_position_samples_start:ping_position_samples_end] += signal_result*signal_ping_scale[i]

# 16 threshold levels
analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]
threshold_levels = [1/x*40 for x in analogue_gains]

# find position of first threshold crossing for each threshold level
threshold_crossings = np.zeros(len(threshold_levels), dtype=np.int32)
for i, threshold_level in enumerate(threshold_levels):
    threshold_crossings[i] = np.argmax(time_response.real > threshold_level)

print('Threshold crossings: ', threshold_crossings)

pseudo_signal = ptd.PseudoTimeDomain(8, 20)
pseudo_signal.positionPings2D([threshold_crossings], signal_length_seconds*1e6)


# plot the time domain response and the threshold crossings on the same plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot((time_response))
ax.plot(threshold_crossings, (time_response[threshold_crossings]), 'o')
# plot line from x axis to threshold crossing
for i, threshold_crossing in enumerate(threshold_crossings):
    ax.plot([threshold_crossing, threshold_crossing], [0, (time_response[threshold_crossing])], 'k-')
    # plot line from y axis to threshold crossing
    ax.plot([0, threshold_crossing], [(time_response[threshold_crossing]), (time_response[threshold_crossing])], 'k-')
ax.set_xlabel('Time')
ax.set_ylabel('Signal strength')

# plot the pseudo time domain response
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.arange(0, pseudo_signal.signal_end, 1/pseudo_signal.sample_frequency), pseudo_signal.distance_responses)
ax.set_xlabel('Time')
ax.set_ylabel('Signal strength')

# plot the responses together
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time_response)
ax.plot(np.arange(0, pseudo_signal.signal_end, 1/pseudo_signal.sample_frequency), pseudo_signal.signal_responses)

plt.show()