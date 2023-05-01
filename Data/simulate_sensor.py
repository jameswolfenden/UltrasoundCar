import numpy as np
from scipy.fft import ifft, fft, fftfreq
import math
import matplotlib.pyplot as plt
import scipy.signal as signal
import pseudotimedomain as ptd



sample_frequency = 10e6
signal_length_seconds = 0.0005
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
signal_ping_position = [0.00018,  0.00035]
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
#threshold_levels = [0.01945474, 0.0287453,  0.03803586, 0.04732642, 0.05661698, 0.0751981, 0.09377923, 0.11236035, 0.16810371, 0.21455651, 0.26100931, 0.30746212, 0.35391492, 0.44682052, 0.53972613, 0.63263173]

# find position of first threshold crossing for each threshold level
threshold_crossings = np.zeros(len(threshold_levels), dtype=np.int32)
for i, threshold_level in enumerate(threshold_levels):
    threshold_crossings[i] = np.argmax(time_response.real > threshold_level)

print('Threshold crossings: ', threshold_crossings)

pseudo_signal = ptd.PseudoTimeDomain(8, 20)
pseudo_signal.positionPings2D([np.int32(threshold_crossings/10)], signal_length_seconds*1e6)


# plot the time domain response and the threshold crossings on the same plot
plt.figure(figsize=(5, 4))
plt.plot([], label="Signal", linewidth=1, color='tab:blue')
plt.plot([], label="Threshold levels", linewidth=1, color='tab:green')
plt.plot([], 'x', label="Threshold crossings", color='tab:red')
#plt.plot([], 'r:', label="Threshold crossing positions")
plt.plot(time,time_response, linewidth=1, color='tab:blue')
# plot line from x axis to threshold crossing
for i, threshold_crossing in enumerate(threshold_crossings):
    #plt.plot([time[threshold_crossing], time[threshold_crossing]], [0, threshold_levels[i]], 'r:', linewidth=1)
    # plot line from y axis to threshold crossing
    plt.plot([0, time[threshold_crossing]], [threshold_levels[i], threshold_levels[i]], '-', linewidth=1, color='tab:green')
plt.plot(time[threshold_crossings], threshold_levels, 'x', color='tab:red')
plt.xlabel('Time (μs)')
plt.ylabel('Relative Amplitude')
plt.legend(loc='lower left')
plt.subplots_adjust(left=0.15, right=0.98, bottom=0.15, top=0.92)
plt.title('Sensor Threshold Interactions with a Signal')

# plot the responses together
fig = plt.figure(figsize=(3.1, 3))
#plt.plot(time,time_response)
plt.plot(np.arange(0, pseudo_signal.signal_end, 1/pseudo_signal.sample_frequency), pseudo_signal.signal_responses, linewidth=1, color='tab:blue')
plt.xlabel('Time (μs)')
plt.ylabel('Relative Amplitude')
plt.title('Reproduced Signal')
plt.ylim(-1.1, 1.1)
plt.xlim(0, 430)
fig.subplots_adjust(left=0.25, right=0.95, bottom=0.15, top=0.85)
plt.savefig('newsig.svg')

# plot signal_result
fig = plt.figure(figsize=(3.1,3))
plt.plot(np.arange(0, len(signal_result), 1)/sample_frequency*1e6, signal_result.real, linewidth=1, color='tab:blue')
plt.xlabel('Time (μs)')
plt.ylabel('Relative Amplitude')
plt.title('Synthesised Wave Packet')
plt.ylim(-1.1, 1.1)
# increase left and right margins to fit the title
fig.subplots_adjust(left=0.25, right=0.95, bottom=0.15, top=0.85)
plt.savefig('packet.svg')


plt.show()