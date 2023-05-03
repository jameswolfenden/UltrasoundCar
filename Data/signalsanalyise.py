# program to read in time signals from a file and analyse them.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.font_manager as fm

fm.fontManager.addfont('C:\\Users\\wolfe\\AppData\\Local\\Microsoft\\Windows\\Fonts\\cmunrm.ttf')

valid_gains = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16] # 12 is broken
#valid_gains = [1, 16]
analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]
# use only the valid gains
analogue_gains_new = [analogue_gains[i-1] for i in valid_gains]

detected_times = [4153, 4157, 4130, 4133, 4129, 4108, 4105, 4108, 4083, 3147, 3024, 2459, 2949, 2410, 2381, 2360]
detected_times_new = [detected_times[i-1] for i in valid_gains]
#detected_times_new = [4025, 4005, 4002, 4005, 4001, 3980, 2641, 2716, 2440, 2435, 2368, 2387, 2335, 2314, 2285, 2285] # idk


outer_pulses = []
outer_means = []
outer_peaks = []
# read in the data from the csv file for each gain
for gain in valid_gains:
    # read in the data from the csv file
    data = pd.read_csv('plate70pole40gain' + str(gain) + '.csv')
    # find the indexes where ch1 is below 0.5
    indexes = np.where(data['Ch1'] < 0.5)[0]
    # find the indexes where the next value of ch1 is above 0.5
    indexes = indexes[np.where(data['Ch1'][indexes+1] > 0.5)[0]]
    min_gap = 10000
    final_indexes = [0]
    for i in indexes:
        gap = i - final_indexes[-1]
        if gap > min_gap:
            final_indexes.append(i+1)

    # split the data into the individual pulses
    inner_pulses = []
    inner_means = []
    inner_peaks = []
    for i in range(len(final_indexes)-1):
        # get ch2 as numpy array
        ch2 = data['Ch2'][final_indexes[i]:final_indexes[i+1]].values
        # append to the list of pulses
        inner_pulses.append(ch2)
        mean = np.mean(ch2)
        inner_means.append(mean)
        peaks = [np.max(ch2[2395:2408]), np.max(ch2[2370:2383]), np.max(ch2[2345:2358]), np.max(ch2[2370:2383]), np.max(ch2[2420:2433]), np.max(ch2[2987:3000]), np.max(ch2[3010:3023])]
        inner_peaks.append(peaks)
    outer_pulses.append(inner_pulses)
    outer_means.append(inner_means)
    outer_peaks.append(inner_peaks)

outer_means = np.array(outer_means)
outer_peaks = np.array(outer_peaks)

# find median of all means
median_means = np.median(outer_means.flatten())
print(median_means)

# find mean of the peaks for each peak location
mean_peaks = np.mean(outer_peaks, axis=0)
print(mean_peaks)

# find median of the peaks relative to the mean for each gain
median_peaks = np.median(np.median((outer_peaks-median_means)/mean_peaks, axis=2), axis=1)
median_peaks = median_peaks/median_peaks[-1]
print(median_peaks)

# fit line median peaks against analogue gains
fit = np.polyfit(analogue_gains_new, median_peaks, 1)
print(fit)

gain_scales = (np.array(analogue_gains)*fit[0] + fit[1])
gain_scales = gain_scales/gain_scales[-1]
print(gain_scales)

# plot the median peaks against the analogue gain and the fit
plt.figure(figsize=(5,3.5))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot(analogue_gains, fit[0]*np.array(analogue_gains) + fit[1], linewidth=2)
plt.plot(analogue_gains_new, median_peaks, 'x', linewidth=2, color='tab:red')
plt.plot(analogue_gains[11], fit[0]*np.array(analogue_gains[11]) + fit[1], 'x', linewidth=2, color='tab:red')
#plt.plot(analogue_gains, fit[0]*np.array(analogue_gains) + fit[1], '.')
# set xlim
plt.xlim(0, 720)
plt.subplots_adjust(left=0.12, right=0.98, top=0.92, bottom=0.13)
plt.title('Relative Amplitude Against Analogue Gain')
plt.xlabel('Analogue Gain')
plt.ylabel('Relative Amplitude')
plt.show()


# plot the log of the median peaks against the gain
plt.figure()
plt.plot(valid_gains, np.log(median_peaks))
plt.xlabel('Gain')
plt.ylabel('Log Median Peak')
plt.show()

# plot the last pulse for the first gain
to_plot = outer_pulses[0][1][0:5000]-median_means
plt.figure(figsize=(7,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot([], label="Signal", linewidth=2, color='tab:blue')
plt.plot([], label="Lowest Gain Output", linewidth=2, color='tab:green')
plt.plot([], label="Other Gain Outputs", linewidth=0.3, color='tab:red')
plt.xlabel('Time (μs)')
plt.ylabel('Signal Amplitude (V)')
plt.title('Lowest Gain')
plt.ylim(-3,3)
plt.xlim(0,5000)
plt.minorticks_on()
plt.subplots_adjust(left=0.08, right=0.97, top=0.92, bottom=0.15)
# plot vertical line at the detected times
for i in range(len(detected_times)):
    plt.axvline(detected_times[i], color='tab:red', linewidth=0.3)
plt.axvline(detected_times[0], color='tab:green', linewidth=2)
plt.plot(to_plot, linewidth=2, color='tab:blue')
plt.legend(loc='upper center')

# plot the last pulse for the last gain
to_plot = outer_pulses[-1][1][0:5000]-median_means
plt.figure(figsize=(7,3))
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["CMU Serif"]
plt.rc('axes', unicode_minus=False)
plt.plot([], label="Signal", linewidth=2, color='tab:blue')
plt.plot([], label="Highest Gain Output", linewidth=2, color='tab:green')
plt.plot([], label="Other Gain Outputs", linewidth=0.3, color='tab:red')
plt.xlabel('Time (μs)')
plt.ylabel('Signal Amplitude (V)')
plt.title('Highest Gain')
plt.ylim(-3, 3)
plt.xlim(0, 5000)
plt.minorticks_on()
plt.subplots_adjust(left=0.08, right=0.97, top=0.92, bottom=0.15)
# plot vertical line at the detected times
for i in range(len(detected_times)):
    plt.axvline(detected_times[i], color='tab:red', linewidth=0.3)
plt.axvline(detected_times[-1], color='tab:green', linewidth=2)
plt.plot(to_plot, linewidth=2, color='tab:blue')
plt.legend(loc='upper center')
plt.show()

# plot the individual pulses on the same graph
for i in range(len(outer_pulses)):
    #for j in range(len(outer_pulses[i])):
    plt.plot((outer_pulses[i][10][0:5000]-median_means))
# plot vertical line at the detected times
for i in range(len(detected_times_new)):
    plt.axvline(detected_times_new[i], color='r')
plt.show()


# plot the individual pulses on the same graph, scaled by the fit for the gain
for i in range(len(outer_pulses)):
    #for j in range(len(outer_pulses[i])):
    plt.plot((outer_pulses[i][1][2000:5000]-median_means)/(analogue_gains_new[i]*fit[0] + fit[1]))
# plot vertical line at the detected times
for i in range(len(detected_times_new)):
    plt.axvline(detected_times_new[i]-2000, color='r')
to_plot_gains = gain_scales*1
# plot a point at x=0, y=to_plot_gains for each gain
plt.plot([np.zeros_like(to_plot_gains), to_plot_gains], 'o')
plt.show()

