import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from scipy.signal import hilbert

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')

# read in from csv file
data = pd.read_csv('distance.csv')

time = data.iloc[:,0]
pressures = data.iloc[:,1:]

# distance vector - name of each column after the first before a space
distances = pressures.columns
distances = [float(distance[:distance.find(' ')]) for distance in distances]
print(distances)

# replace nan with 0
pressures = pressures.fillna(0)

# perform hilbert transform on each pressure
for i in range(pressures.shape[1]):
    pressures.iloc[:,i] = hilbert(pressures.iloc[:,i])

# find the peak of each pressure after 300 μs
peak = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    peak[i] = max(abs(pressures.iloc[300:,i]))

print(peak)

# read in data from csv
data = pd.read_csv('attenuation.csv')

#first column is distance, second column is peak
distances = data.iloc[:,0]
peak = data.iloc[:,1]


# plot data, first column is the x axis, second column is the y axis
plt.figure(figsize=(7,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(distances, peak/peak.iloc[0], label='Peak of Responses')

plt.xlabel('Distance (cm)')
plt.ylabel('Normalised Acoustic Pressure')

# set margins
plt.subplots_adjust(left=0.07, right=0.97, top=0.97, bottom=0.15)

# work out the attenuation coefficient
mu = 0.115 # Np/m
distances = np.linspace(min(distances), max(distances), 100)
attenuation = np.exp(-mu*distances*2/100)
plt.plot(distances, attenuation/attenuation[0], label='Attenuation', color='k', linestyle='--', linewidth=0.75)
plt.legend(loc='lower left')
#plt.ylim(0,1.1)

plt.show()
