import numpy as np
from scipy import signal
from scipy.fft import fft, fftshift, ifft
import matplotlib.pyplot as plt
import math


gain_time = [2825,2780,2801,2780,2776,2723,2680,2699,2629,1906,1831,1827,1833,1833,1833,1833]


frequency = 40000
cycles = 5
points_per_cycle = 5
ping_duration = cycles/frequency
print(ping_duration)
sample_frequency = frequency*points_per_cycle
signal_duration = 1200

signal_responses = np.zeros(signal_duration*sample_frequency)


ifft_result = ifft([0,points_per_cycle,0], points_per_cycle)
signal_result = np.tile(ifft_result,cycles)
t = np.arange(cycles*points_per_cycle)

window = signal.windows.hann(cycles*points_per_cycle)
ping_shape = np.multiply(window,signal_result)


for i_ping, ping in enumerate(gain_time):
    signal_responses[(ping-1700)*sample_frequency-math.ceil(cycles*points_per_cycle/2):(ping-1700)*sample_frequency+int(cycles*points_per_cycle/2)] = ping_shape*(1-0.05*i_ping)

plt.plot(np.arange(signal_responses.size),signal_responses)

plt.figure()
plt.plot(t, ping_shape.real, 'b-', t, ping_shape.imag, 'r--', t, abs(ping_shape))
plt.legend(('real', 'imaginary', 'abs'))
plt.show()


print("end")