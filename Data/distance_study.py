import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')

# read in from csv file
data = pd.read_csv('distancepara.csv')

time = data.iloc[:,0]
distance35 = data.iloc[:,1].to_numpy()/0.021
distance20 = data.iloc[:,2].to_numpy()/0.021
distance5 = data.iloc[:,3].to_numpy()/0.021
distance20[2000:2501]=distance20[300:801]
distance5[2000:2501]=distance5[1250:1751]

# plot data, first column is the x axis, second column is the y axis
fig = plt.figure(figsize=(7,4))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)

gs = fig.add_gridspec(3, hspace=0.1)
axs = gs.subplots(sharex=True, sharey=True)
axs[0].plot(time, distance5, label='5 cm')
axs[1].plot(time, distance20, label='20 cm')
axs[2].plot(time, distance35, label='35 cm')
# set x and y lims
axs[0].set_ylim(-1.1,1.1)
axs[0].set_xlim(0,2500)

# set x and y labels
axs[2].set_xlabel('Time (μs)')
axs[1].set_ylabel('Normalised Acoustic Pressure')

# show legends
axs[0].legend(loc='lower right')
axs[1].legend(loc='lower right')
axs[2].legend(loc='lower right')

# set margins
plt.subplots_adjust(left=0.07, right=0.97, top=0.97, bottom=0.13)

# Hide x labels and tick labels for all but bottom plot.
for ax in axs:
    ax.label_outer()

plt.show()