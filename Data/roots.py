import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from scipy.signal import hilbert

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')

# read in from csv file
data = pd.read_csv('roots.csv')

time = data.iloc[:,0]
pressures = data.iloc[:,1:]

# radius vector - name of each column after the first before a space
radius = pressures.columns
radius = [float(radius[:radius.find(' ')]) for radius in radius]
print(radius)

# perform hilbert transform on each pressure
for i in range(pressures.shape[1]):
    pressures.iloc[:,i] = hilbert(pressures.iloc[:,i])

# find the peak of each pressure after 300 μs
peak = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    peak[i] = max(abs(pressures.iloc[300:,i]))

# plot peak against radius
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(radius, peak/peak[-1], label='Peak of Responses')

plt.xlabel('Radius (cm)')
plt.ylabel('Normalised Acoustic Pressure')
plt.xticks([0,1,2,3,4,5,6,7])
# set margins
plt.subplots_adjust(left=0.16, right=0.97, top=0.97, bottom=0.16)
plt.savefig('rootsnap.svg')

plt.show()

# find time to the first part of each pressure after 300 μs greater than half the peak
timehalf = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    timehalf[i] = time[np.where(abs(pressures.iloc[300:720,i]) > peak[i]*0.1)[0][0]+300]
print(timehalf)

# plot timehalf against radius
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(radius, timehalf, label='Time to Half Peak')

plt.xlabel('Radius (cm)')
plt.ylabel('Time to Half Peak (μs)')

# set margins
plt.subplots_adjust(left=0.16, right=0.97, top=0.97, bottom=0.16)
plt.savefig('rootstof.svg')

plt.show()

# plot all pressures
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
for i in range(pressures.shape[1]):
    plt.plot(time, pressures.iloc[:,i], label='r = '+str(radius[i])+' cm')

plt.xlabel('Time (μs)')
plt.ylabel('Acoustic Pressure')

plt.legend()

plt.show()


