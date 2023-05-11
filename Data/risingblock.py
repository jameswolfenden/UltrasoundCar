import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from scipy.signal import hilbert

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')

# read in from csv file
data = pd.read_csv('risingblock.csv')

time = data.iloc[:,0]
pressures = data.iloc[:,1:]

# motion vector - name of each column after the first
motion = pressures.columns
# find the value of motion before a space
motion = [float(motion[:motion.find(' ')]) for motion in motion]
print(motion)

# perform hilbert transform on each pressure
for i in range(pressures.shape[1]):
    pressures.iloc[:,i] = hilbert(pressures.iloc[:,i])

# find the peak of each pressure after 300 μs
peak = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    peak[i] = max(abs(pressures.iloc[600:,i]))

# plot peak against motion
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(motion, peak/max(peak), label='Peak of Responses')

plt.xlabel('Sludge Blockage Height (cm)')
plt.ylabel('Normalised Acoustic Pressure')
plt.xticks(np.arange(0, 15.1, 2.5))
# set margins
plt.subplots_adjust(left=0.16, right=0.97, top=0.97, bottom=0.16)
plt.savefig('risingblocknap.svg')

plt.show()

# plot all pressures
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
for i in range(pressures.shape[1]):
    plt.plot(time, pressures.iloc[:,i], label=str(motion[i])+' cm')
plt.legend()

plt.xlabel('Time (μs)')
plt.ylabel('Acoustic Pressure')

plt.show()

# find time to the first part of each pressure after 300 μs greater than half the peak
timehalf = np.zeros(pressures.shape[1])
for i in range(pressures.shape[1]):
    timehalf[i] = time[np.where(abs(pressures.iloc[600:,i]) > peak[i]*0.4)[0][0]+600]
print(timehalf)

# plot timehalf against motion
plt.figure(figsize=(3.3,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(motion, timehalf, label='Time to Half Peak')

plt.xlabel('Sludge Blockage Height (cm)')
plt.ylabel('Time of Flight (μs)')
plt.xticks(np.arange(0, 15.1, 2.5))
# set margins
plt.subplots_adjust(left=0.16, right=0.97, top=0.97, bottom=0.16)
plt.savefig('risingblocktof.svg')

plt.show()