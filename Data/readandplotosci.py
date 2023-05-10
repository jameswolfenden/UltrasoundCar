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
plt.plot(time, to_plot/max(to_plot), label='Experimental Response')
plt.axvline(x=620, color='k', linestyle='--', linewidth=0.75)
plt.axvline(x=1410, color='k', linestyle='--', linewidth=0.75)
plt.plot([500, 855], [0.3655, 0.3655], color='tab:red', linestyle='-', linewidth=1)
plt.plot([500, 1920], [1, 1], color='tab:red', linestyle='-', linewidth=1)
plt.plot([], [], color='tab:red', linestyle='-', linewidth=1, label='Peak of Responses')
plt.plot([], [], color='k', linestyle='--', linewidth=0.75, label='Times of Flight')
plt.legend(bbox_to_anchor=(0.25, 0.35))
plt.xlabel('Time (μs)')
plt.ylabel('Relative Amplitude')
# set x limits
plt.xlim(500,2500)
# set y limits
plt.ylim(-1.1,1.1)
plt.minorticks_on()
plt.subplots_adjust(left=0.1, right=0.97, top=0.92, bottom=0.15)
plt.show()