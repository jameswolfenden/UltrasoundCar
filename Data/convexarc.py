import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from scipy.signal import hilbert

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')

# read in from csv file
data = pd.read_csv('convexarc.csv')

time = data.iloc[:,0]
pressures = data.iloc[:,1:]

data2 = pd.read_csv('slant2.csv')
pressures_flat = data2.iloc[:,1]

# remove the second pressure
pressures.drop(pressures.columns[1], axis=1, inplace=True)

# arc vector - name of each column after the first
arcs = pressures.columns
# find the value of arcs after the characters 'arc'
arcs = [float(arc[arc.find('arc')+3:]) for arc in arcs]
print(arcs)

# perform hilbert transform on each pressure
for i in range(pressures.shape[1]):
    pressures.iloc[:,i] = hilbert(pressures.iloc[:,i])
pressures_flat = hilbert(pressures_flat)

# find the peak of each pressure after 300 μs
peak = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    peak[i] = max(abs(pressures.iloc[300:,i]))
peak_flat = max(abs(pressures_flat[300:]))

# plot peak against arc
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(arcs, peak/peak[-1], label='Peak of Responses')
plt.ylabel('Normalised Acoustic Pressure')
plt.xlabel('Arc Radius (cm)')

# set margins
plt.subplots_adjust(left=0.16, right=0.97, top=0.97, bottom=0.16)
plt.savefig('convexarcnap.svg')

plt.show()


# find time to the first part of each pressure after 300 μs greater than half the peak
timehalf = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    timehalf[i] = time[np.where(abs(pressures.iloc[300:,i]) > peak[i]*0.1)[0][0]+300]
print(timehalf)

#plot all pressures
plt.figure(figsize=(7,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
for i in range(pressures.shape[1]):
    plt.plot(time, (pressures.iloc[:,i]), label=str(arcs[i])+'cm')
plt.plot(time, pressures_flat, label='Flat')
plt.legend(loc='upper right')
plt.xlabel('Time (μs)')
plt.ylabel('Acoustic Pressure (Pa)')
plt.show()


# plot timehalf against arc
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(arcs, timehalf, label='Time to Half Peak')
plt.xlabel('Angle (°)')
plt.ylabel('Time of Flight (μs)')

# set margins
plt.subplots_adjust(left=0.15, right=0.97, top=0.97, bottom=0.16)

plt.show()