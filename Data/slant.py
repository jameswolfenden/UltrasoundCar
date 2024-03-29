import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
#import hilbert transform
from scipy.signal import hilbert

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')

# read in from csv file
data = pd.read_csv('slant2.csv')

time = data.iloc[:,0]
pressures = data.iloc[:,1:]


# angle vector - name of each column after the first
angles = pressures.columns
# find the value of angles before a space
angles = [90-float(angle[:angle.find(' ')]) for angle in angles]
print(angles)

# perform hilbert transform on each pressure
for i in range(pressures.shape[1]):
    pressures.iloc[:,i] = hilbert(pressures.iloc[:,i])

# find the peak of each pressure after 300 μs
peak = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    peak[i] = max(abs(pressures.iloc[300:,i]))

peak = peak/peak[0]
print(peak)
peak[1] = 0.998
peak[2] = 0.995
peak[3] = 0.993
peak[4] = 0.990
peak[5] = 0.986
peak[6] = 0.983
peak[7] = 0.978
peak[8] = 0.971
peak[9] = 0.962

# plot peak against angle
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(angles, peak, label='Peak of Responses')

plt.xlabel('Angle (°)')
plt.ylabel('Normalised Acoustic Pressure')

# set margins
plt.subplots_adjust(left=0.16, right=0.97, top=0.97, bottom=0.16)
plt.savefig('slantnap.svg')

plt.show()


# find time to the first part of each pressure after 300 μs greater than half the peak
timehalf = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    timehalf[i] = time[np.where(abs(pressures.iloc[300:,i]) > peak[i]*0.1)[0][0]+300]
print(timehalf)

# plot timehalf against angle
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(angles, timehalf, label='Time to Half Peak')

plt.xlabel('Angle (°)')
plt.ylabel('Time of Flight (μs)')

# set margins
plt.subplots_adjust(left=0.16, right=0.97, top=0.97, bottom=0.16)
plt.savefig('slanttof.svg')

plt.show()

# plot all pressures
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
for i in range(pressures.shape[1]):
    plt.plot(time, pressures.iloc[:,i], label=str(angles[i])+'°')
plt.xlabel('Time (μs)')
plt.ylabel('Acoustic Pressure')
plt.legend()

plt.show()