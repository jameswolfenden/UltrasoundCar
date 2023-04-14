# read in csv file using pandas and plot the third column excuding the first row
#
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pseudotimedomain as ptd

# read in csv file
df = pd.read_csv('OscilloscopeBlock.csv', skiprows=1, header=None)

# find the index where the second column is first greater than 1.5
index_start = df[1][df[1] > 1.5].index[0]-1
print(index_start)
index_end = 6750


gains = [[3045, 2950, 2994, 2949, 2873, 2874, 2874, 2848, 2848, 2848, 2848, 2848, 2848, 2848, 2802, 1773, 1773, 1772, 1677, 1772, 1772]]

pseudo_signal = ptd.PseudoTimeDomain(25,25, 0.04, False)
pseudo_signal.positionPings2D(gains,5000)

gains_srf = [[3129, 3076, 1961, 1805, 1664, 1683, 1608, 1587, 1511, 1511, 1511, 1511, 1511, 1511, 1511, 1511]]

pseudo_signal_srf = ptd.PseudoTimeDomain(25,25)
pseudo_signal_srf.positionPings2D(gains_srf,5000)

# plot signal responses and third column
plt.figure()
plt.plot(np.arange(index_end-index_start),df[2][index_start:index_end]-1.54)
plt.plot(pseudo_signal.signal_responses/8)
plt.plot(pseudo_signal_srf.signal_responses/8)
plt.legend(['Signal', 'Pseudo hc', 'Pseudo SRF'])

# plot the distance responses and abs of third column
plt.figure()
plt.plot(np.arange(index_end-index_start),np.abs(df[2][index_start:index_end]-1.54))
plt.plot(pseudo_signal.distance_responses/8)
plt.plot(pseudo_signal_srf.distance_responses/8)
plt.legend(['Signal', 'Pseudo hc', 'Pseudo SRF'])

plt.show()
