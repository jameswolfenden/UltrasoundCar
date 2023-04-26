import numpy as np
import pseudotimedomain as ptd
import matplotlib.pyplot as plt


data = [4153, 4157, 4130, 4133, 4129, 4108, 4105, 4108, 4083, 3147, 3024, 2459, 2949, 2410, 2381, 2360]
data = [1113, 965, 1034, 885, 890, 890, 890, 890, 890, 890, 890, 890, 890, 890, 890, 890]

pseudo_signal = ptd.PseudoTimeDomain(8, 20)
pseudo_signal.positionPings2D([data], 5000)



# plot the pseudo time domain response
plt.figure(figsize=(7,3))
plt.plot(np.arange(0, pseudo_signal.signal_end, 1/pseudo_signal.sample_frequency), pseudo_signal.signal_responses*2.5)
plt.xlabel('Time (μs)')
plt.ylabel('Signal strength')
plt.title('Pseudo Time Domain Response')
plt.ylim(-3,3)
plt.xlim(0,5000)
plt.minorticks_on()
plt.subplots_adjust(left=0.08, right=0.97, top=0.92, bottom=0.15)
plt.show()