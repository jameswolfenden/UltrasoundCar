import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')


# read in from csv file
data = pd.read_csv('felipe.csv')
# plot data, first column is the x axis, second column is the y axis
plt.figure(figsize=(7,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(data.iloc[:,0], data.iloc[:,1]/max(data.iloc[500:,1]))
plt.xlabel('Time (μs)')
plt.ylabel('Relative Amplitude')
#plt.title('Title')
plt.ylim(-1.1,1.1)
plt.xlim(500,2500)
plt.minorticks_on()
plt.subplots_adjust(left=0.1, right=0.97, top=0.92, bottom=0.15)
plt.show()