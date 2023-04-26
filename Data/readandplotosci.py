# read in from csv file and plot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read in csv file
df = pd.read_csv('pipe1020gain1.csv', skiprows=1, header=None)

# plot second and third column against first column
#plt.figure()
#plt.plot(df[0],df[1])
#plt.plot(df[0],df[2])
#plt.legend(['Channel 1', 'Channel 2'])
#plt.show()

#to_plot = df[2][49000:52000]-2.5
to_plot = df[2][47400:50400]-2.5
time = np.arange(0, len(to_plot)) # time in microseconds
print("idk if you want to normalise by 2.5 or nah")

plt.figure()
plt.plot(time, to_plot)
plt.xlabel('Time (μs)')
plt.ylabel('Signal strength (V)')
# turn on grid
plt.grid(True)
# minor grid
plt.minorticks_on()
plt.show()