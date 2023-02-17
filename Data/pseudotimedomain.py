import numpy as np
from scipy import signal
from scipy.fft import ifft
import matplotlib.pyplot as plt
import math
import csv
from pathlib import Path
import os.path


with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "gain_pings.csv"))), newline='') as f:
    reader = csv.reader(f)
    gain_time = list(reader)
gain_time = [eval(i) for i in gain_time[0]]


print(gain_time)

#gain_time = [2825,2780,2801,2780,2776,2723,2680,2699,2629,1906,1831,1827,1833,1833,1833,1833]

analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]

plt.figure()
plt.plot(gain_time, analogue_gains)

plt.figure()
mss = np.zeros(6000)
mss[gain_time] = 1
plt.plot(mss)

frequency = 0.04
cycles = 15
points_per_cycle = 20
ping_duration = cycles/frequency
print(ping_duration)
sample_frequency = frequency*points_per_cycle
signal_duration = 6000

signal_responses = np.zeros(int(signal_duration*sample_frequency))


ifft_result = ifft([0,points_per_cycle,0], points_per_cycle)
signal_result = np.tile(ifft_result,cycles)
t = np.arange(cycles*points_per_cycle)

window = signal.windows.hann(cycles*points_per_cycle)
ping_shape = np.multiply(window,signal_result)

for i_ping, ping in enumerate(gain_time):
    if not ping == 0:
        signal_responses[int(ping*sample_frequency)-math.ceil(cycles*points_per_cycle/2):int(ping*sample_frequency)+int(cycles*points_per_cycle/2)] +=ping_shape.real*1/analogue_gains[i_ping]
    
plt.figure()
plt.plot(np.multiply(np.arange(signal_responses.size),1/sample_frequency*343*10**-6/2),signal_responses)

plt.figure()
plt.plot(t, ping_shape.real, 'b-', t, ping_shape.imag, 'r--', t, abs(ping_shape))
plt.legend(('real', 'imaginary', 'abs'))
plt.show()


print("end")