import numpy as np
import PseudoTimeDomain as ptd
import matplotlib.pyplot as plt


data = [4585, 4556, 4537, 3524, 3176, 3076, 2803, 2435, 2079, 2031, 1584, 1610, 1610, 1610, 1610, 1610]

pseudo_signal = ptd.PseudoTimeDomain(8, 20)
pseudo_signal.positionPings2D([data], 5000)


# plot the pseudo time domain response
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.arange(0, pseudo_signal.signal_end, 1/pseudo_signal.sample_frequency), pseudo_signal.distance_responses)
ax.set_xlabel('Time')
ax.set_ylabel('Signal strength')
plt.show()