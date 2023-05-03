# read in from csv file and plot
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import pandas as pd

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')


# read in csv file
df = pd.read_csv('pipe1025gain1.csv', skiprows=1, header=None)

# plot second and third column against first column
#plt.figure()
#plt.plot(df[0],df[1])
#plt.plot(df[0],df[2])
#plt.legend(['Channel 1', 'Channel 2'])
#plt.show()

#to_plot = df[2][49000:52000]-2.5
#to_plot = df[2][47400:50400]-2.5
to_plot = df[2][52200:55200]-2.5
time = np.arange(0, len(to_plot)) # time in microseconds
print("idk if you want to normalise by 2.5 or nah")

plt.figure(figsize=(7,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(time, to_plot/max(to_plot))
plt.xlabel('Time (μs)')
plt.ylabel('Relative Amplitude')
# set x limits
plt.xlim(500,2500)
# set y limits
plt.ylim(-1.1,1.1)
plt.minorticks_on()
plt.subplots_adjust(left=0.1, right=0.97, top=0.92, bottom=0.15)
plt.show()