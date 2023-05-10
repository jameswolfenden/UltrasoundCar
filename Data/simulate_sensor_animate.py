import numpy as np
from scipy.fft import ifft, fft, fftfreq
import math
import matplotlib.pyplot as plt
import scipy.signal as signal
import pseudotimedomain as ptd
import matplotlib.font_manager as fm
import matplotlib.animation as animation 

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')



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
pseudo_dts = np.zeros((len(threshold_crossings), int(20*0.04*signal_length_seconds*1e6)), dtype=np.complex128)
for i, threshold_crossing in enumerate(threshold_crossings):
    pseudo_signal.positionPings2D([np.int32(threshold_crossings[:i+1]/10)], signal_length_seconds*1e6)
    pseudo_dts[i] = pseudo_signal.signal_responses[:,0]



# animate a figure of each threshold level for each frame
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.set_size_inches(12, 6)
fig.set_dpi(200)
ax1.set_xlim(0, signal_length_seconds*1e6)
ax2.set_xlim(0, signal_length_seconds*1e6)
ax1.set_ylim(-1.1, 1.1)
ax2.set_ylim(-1.1, 1.1)
ax1.plot(time,time_response, linewidth=1, color='tab:blue')
ax1.plot([], label="Real Signal", linewidth=1, color='tab:blue')
ax1.plot([], label="Threshold levels", linewidth=1, color='tab:green')
ax1.plot([], 'x', label="Threshold crossings", color='tab:red')
ax1.set_xlabel('Time (μs)')
ax1.set_ylabel('Relative Amplitude')
ax2.set_xlabel('Time (μs)')
ax2.set_ylabel('Relative Amplitude')
ax1.legend(loc='lower left')
ax2.plot([], label="Reproduced Signal", linewidth=1, color='tab:blue')
ax2.legend(loc='lower left')
line, = ax1.plot([], [], '-', linewidth=1, color='tab:green')
line1, = ax1.plot([], [], 'x', color='tab:red')
line2, = ax2.plot([], [], linewidth=1, color='tab:blue')

def init():
    line.set_data([], [])
    line2.set_data([], [])
    line1.set_data([], [])
    return line, line2, line1

def animate(i):
    if i == 0:
        line2.set_data([0,1000], [0,0])
    else:
        line.set_data([0, time[threshold_crossings[i-1]]], [threshold_levels[i-1], threshold_levels[i-1]])
        line1.set_data(time[threshold_crossings[:i]], threshold_levels[:i])
        line2.set_data(np.arange(0, pseudo_signal.signal_end, 1/pseudo_signal.sample_frequency), pseudo_dts[i-1,:])
    return line,line2,line1

anim = animation.FuncAnimation(fig, animate, init_func=init,
                                 frames=len(threshold_levels)+1, interval=1000, blit=True)
anim.save('test.mp4', writer = 'ffmpeg', fps = 1, bitrate=-1)
#plt.show()