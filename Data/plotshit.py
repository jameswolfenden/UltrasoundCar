# read in csv file using pandas and plot the third column excuding the first row
#
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import scipy fft
from scipy.fftpack import fft, ifft

# read in csv file
df = pd.read_csv('OscilloscopeBlock.csv', skiprows=1, header=None)

# find the index where the third column is first greater than 1.5
index_start = df[2][df[2] > 1.5].index[0]
print(index_start)
index_end = 9000

sample_freq = 1e6 # 1 MHz

# fft of the forth column past the index
yf = fft(df[3][index_start:index_end].values)
xf = np.linspace(0.0, sample_freq/2, (index_end-index_start)//2)

# ifft of the fft of the forth column, cropped to max frequency of 50 kHz
yf_ifft = ifft(yf[np.where(xf<10000)[0][-1]:np.where(xf>50000)[0][0]])

# plot the ifft of the fft of the forth column
plt.figure()
plt.plot(yf_ifft)
plt.title('IFFT of the FFT of the forth column')

# plot the fft
plt.figure()
plt.plot(xf, 2.0/(index_end-index_start) * np.abs(yf[0:(index_end-index_start)//2]))
plt.grid()
plt.title('FFT of the forth column')

# plot the third column
plt.figure()
plt.plot(df[2][index_start:index_end])
plt.title('Third column')

# plot the forth column
plt.figure()
plt.plot(df[3][index_start:index_end])
plt.title('Forth column')

# plot the fith column
plt.figure()
plt.plot(df[4][index_start:index_end])
plt.title('Fith column')


# show the plots
plt.show()

