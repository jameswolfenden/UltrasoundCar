import numpy as np
import PseudoTimeDomain as ptd
import os.path
import csv
from pathlib import Path
import matplotlib.pyplot as plt


# use the total focusing method to find the responses in 3d space

# create a 3d meshgrid
x = np.linspace(-0.2,0.2,11)
y = np.linspace(-0.2,0.2,11)
z = np.linspace(0.0,0.4,11)
X,Y,Z = np.meshgrid(x,y,z)

dx = x[1]-x[0]
dy = y[1]-y[0]
dz = z[1]-z[0]

x_edges = np.append(x,x[-1]+dx)-dx/2
y_edges = np.append(y,y[-1]+dy)-dy/2
z_edges = np.append(z,z[-1]+dz)-dz/2
X_edges,Y_edges,Z_edges = np.meshgrid(x_edges,y_edges,z_edges)

# create a PseudoTimeDomain object
pseudo_signal = ptd.PseudoTimeDomain(15,20)


radui = range(5,16,5)
gain_time = []
# load data
for sensor_radius in radui:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "radius_"+str(sensor_radius)+".csv"))), newline='') as f:
        reader = csv.reader(f)
        gain_time_temp = list(reader)
    gain_time_2d = []
    for angle in gain_time_temp:
        gain_time_2d.append([int(i.replace('[','').replace(']','')) for i in angle])
    gain_time.append(gain_time_2d)
sensor_angles = np.arange(0,360, int(360/len(gain_time[0])))

# use the pseudo time domain object to find the responses using the gain time data
pseudo_signal.positionPings2D(gain_time[1],6000) # important the [1]!!!!!!!!!!

# 3d array of zeros to store the responses in the meshgrid
responses = np.zeros((len(x),len(y),len(z)))

aperture_6db_angle = np.radians(70)

sensor_radius = 0.1

# loop through each distance in the pseudo time domain object and find the response at each point in the meshgrid
for t, response_t in enumerate(pseudo_signal.distance_responses):
    hypotenuse = pseudo_signal.distance[t]/100
    hypotenuse = 0.1
    response_t=[1]
    for angle, response_a in enumerate(response_t):
        radius_of_aperture = hypotenuse*np.sin(aperture_6db_angle/2)
        sensor_position_x = sensor_radius*np.sin(np.radians(sensor_angles[angle]))
        sensor_position_y = sensor_radius*np.cos(np.radians(sensor_angles[angle]))

        distance_to_sensor_edges = np.sqrt((X_edges-sensor_position_x)**2 + (Y_edges-sensor_position_y)**2 + Z_edges**2)
        edges_before_hypotenuse = distance_to_sensor_edges < hypotenuse
        edges_after_hypotenuse = distance_to_sensor_edges >= hypotenuse
        cells_after_hypotenuse = np.logical_and(edges_after_hypotenuse[:-1,:-1,:-1],edges_after_hypotenuse[1:,:-1,:-1])
        cells_after_hypotenuse = np.logical_and(cells_after_hypotenuse,edges_after_hypotenuse[:-1,1:,:-1])
        cells_after_hypotenuse = np.logical_and(cells_after_hypotenuse,edges_after_hypotenuse[:-1,:-1,1:])
        cells_after_hypotenuse = np.logical_and(cells_after_hypotenuse,edges_after_hypotenuse[1:,1:,-1])
        cells_after_hypotenuse = np.logical_and(cells_after_hypotenuse,edges_after_hypotenuse[1:,-1,1:])
        cells_after_hypotenuse = np.logical_and(cells_after_hypotenuse,edges_after_hypotenuse[-1,1:,1:])
        cells_after_hypotenuse = np.logical_and(cells_after_hypotenuse,edges_after_hypotenuse[1:,1:,1:])

        cells_before_hypotenuse = np.logical_and(edges_before_hypotenuse[:-1,:-1,:-1],edges_before_hypotenuse[1:,:-1,:-1])
        cells_before_hypotenuse = np.logical_and(cells_before_hypotenuse,edges_before_hypotenuse[:-1,1:,:-1])
        cells_before_hypotenuse = np.logical_and(cells_before_hypotenuse,edges_before_hypotenuse[:-1,:-1,1:])
        cells_before_hypotenuse = np.logical_and(cells_before_hypotenuse,edges_before_hypotenuse[1:,1:,-1])
        cells_before_hypotenuse = np.logical_and(cells_before_hypotenuse,edges_before_hypotenuse[1:,-1,1:])
        cells_before_hypotenuse = np.logical_and(cells_before_hypotenuse,edges_before_hypotenuse[-1,1:,1:])
        cells_before_hypotenuse = np.logical_and(cells_before_hypotenuse,edges_before_hypotenuse[1:,1:,1:])

        cells_in_aperture = np.logical_and(np.logical_not(cells_after_hypotenuse),np.logical_not(cells_before_hypotenuse))
        responses[cells_in_aperture] = +response_a

# plot edges before and after hypotenuse
fig, axs = plt.subplots(1,2)
axs[0].imshow(edges_before_hypotenuse[:,:,0])
axs[1].imshow(edges_after_hypotenuse[:,:,0])

# plot cells before and after hypotenuse and in aperture
fig, axs = plt.subplots(1,3)
axs[0].imshow(cells_before_hypotenuse[:,:,0])
axs[1].imshow(cells_after_hypotenuse[:,:,0])
axs[2].imshow(cells_in_aperture[:,:,0])
plt.show()

# plot each response in z in 2d using imshow on its own plot in the same figure and laebl the plot with the z value
fig, axs = plt.subplots(5,5)
for i in range(len(z)):
    axs[int(i/5),i%5].imshow(responses[:,:,i])
    axs[int(i/5),i%5].set_title('z = ' + str(z[i]))
plt.show()


# replace 0s with nans
responses[responses==0] = np.nan


# plot the responses in 3d using scatter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X,Y,Z,c=responses)
plt.show()
