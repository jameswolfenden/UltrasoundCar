import numpy as np
from scipy.fft import ifft, fft, fftfreq
import math
import matplotlib.pyplot as plt
import scipy.signal as signal
import pseudotimedomain as ptd



sample_frequency = 10e6
signal_length_seconds = 0.0004
sin_frequency = 40e3
cycles = 8
attenuation_rate = 0.6 # dB/m
points_per_cycle = int(sample_frequency/sin_frequency)

# create an array of zeros to store the time domain response
time_response = np.zeros(int(sample_frequency*signal_length_seconds), dtype=np.complex128)
time = np.linspace(0, signal_length_seconds, len(time_response))*1e6


ifft_result = ifft([0,points_per_cycle,0], points_per_cycle)
signal_result = np.tile(ifft_result,cycles)
window = signal.windows.hann(cycles*points_per_cycle)
signal_result = signal_result*window

#signal_ping_position = np.arange(0.0002, signal_length_seconds-0.0002, 0.0001)
# generate a random scale for each ping
#signal_ping_scale = np.random.rand(len(signal_ping_position))
signal_ping_position = [0.00015,  0.0003]
signal_ping_scale = [0.5, 1]

for i, ping_position in enumerate(signal_ping_position):
    ping_position_samples = int(ping_position*sample_frequency)
    ping_position_samples_start = ping_position_samples - math.floor(cycles*points_per_cycle/2)
    ping_position_samples_end = ping_position_samples + math.ceil(cycles*points_per_cycle/2)
    time_response[ping_position_samples_start:ping_position_samples_end] += signal_result*signal_ping_scale[i]

# apply attenuation
#time_response = time_response*np.exp(attenuation_rate*np.arange(0, len(time_response))/sample_frequency*343*(10**-6)/2)

fftthat = fft(time_response)
freqs = fftfreq(len(time_response), 1/sample_frequency)
plt.plot(freqs, np.abs(fftthat))

# 16 threshold levels
analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]
threshold_levels = [1/x*40 for x in analogue_gains]
threshold_levels = np.linspace(0.3, 0.9, 8)

# find position of first threshold crossing for each threshold level
threshold_crossings = np.zeros(len(threshold_levels), dtype=np.int32)
for i, threshold_level in enumerate(threshold_levels):
    threshold_crossings[i] = np.argmax(time_response.real > threshold_level)

print('Threshold crossings: ', threshold_crossings)

pseudo_signal = ptd.PseudoTimeDomain(8, 20)
pseudo_signal.positionPings2D([np.int32(threshold_crossings/10)], signal_length_seconds*1e6)


# plot the time domain response and the threshold crossings on the same plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([], 'b', label="Signal", linewidth=1)
ax.plot([], 'g', label="Threshold levels", linewidth=1)
ax.plot([], 'rx', label="Threshold crossings")
#ax.plot([], 'r:', label="Threshold crossing positions")
ax.plot(time,time_response, 'b', linewidth=1)
# plot line from x axis to threshold crossing
for i, threshold_crossing in enumerate(threshold_crossings):
    #ax.plot([time[threshold_crossing], time[threshold_crossing]], [0, threshold_levels[i]], 'r:', linewidth=1)
    # plot line from y axis to threshold crossing
    ax.plot([0, time[threshold_crossing]], [threshold_levels[i], threshold_levels[i]], 'g-', linewidth=1)
ax.plot(time[threshold_crossings], threshold_levels, 'rx')
ax.set_xlabel('Time (μs)')
ax.set_ylabel('Response')
ax.legend()
ax.set_title('Sensor Threshold Interactions with a Signal')

# plot the responses together
fig = plt.figure(figsize=(3, 3))
ax = fig.add_subplot(111)
#ax.plot(time,time_response)
ax.plot(np.arange(0, pseudo_signal.signal_end, 1/pseudo_signal.sample_frequency), pseudo_signal.signal_responses, 'b', linewidth=1)
ax.set_xlabel('Time (μs)')
ax.set_ylabel('Response')
ax.set_title('Reproduced Signal')
fig.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.85)
plt.savefig('newsig.svg')

# plot signal_result
fig = plt.figure(figsize=(3,3))
ax = fig.add_subplot(111)
ax.plot(np.arange(0, len(signal_result), 1)/sample_frequency*1e6, signal_result.real, 'b', linewidth=1)
ax.set_xlabel('Time (μs)')
ax.set_ylabel('Response')
ax.set_title('Synthesised Wave Packet')
# increase left and right margins to fit the title
fig.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.85)
plt.savefig('packet.svg')


plt.show()