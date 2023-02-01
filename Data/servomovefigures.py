import matplotlib.pyplot as plt
import numpy as np
import csv

list1 = [1, 2, 3, 4, 5, 6]
list2 = [11, 23, 3, 4, 5, 6]

list3 = []
list3.append(list1)
list3.append(list2)
list3.append(list1)
list3.append(list1)
list3.append(list2)


print(str(list3))

for w in range(len(list3[0:])):
    print(str(list3[w])[1:-1] + "\n")



with open('Data/list_data.csv', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

dataArray = np.array(data).astype("float")



fig, ax = plt.subplots()
im = ax.pcolormesh(range(90, -91, -10), range(1,12,1),  dataArray, cmap="Greys_r", vmax = 250, vmin = 0)

plt.colorbar(im)


plt.show()
