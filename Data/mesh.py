import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')


# read in from csv file
data = pd.read_csv('mesh.csv')
# plot data, first column is the x axis, second column is the y axis
plt.figure(figsize=(5,3.5))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(data.iloc[:,0], data.iloc[:,1], marker='o', markersize=3, linewidth=0.5)
plt.plot(data.iloc[:,0], data.iloc[:,2], marker='o', markersize=3, linewidth=0.5)
plt.xlabel('Mesh Elements per Wavelength')
plt.ylabel('Error (%)')
#plt.title('Title')
#plt.ylim(-1.1,1.1)
#plt.xlim(0,2500)
plt.minorticks_on()
plt.subplots_adjust(left=0.12, right=0.98, top=0.92, bottom=0.13)
plt.legend(['Average Error', 'Max Error'])
# add horizontal line at y=10
plt.axhline(y=10, color='k', linestyle='--', linewidth=0.7)
plt.show()