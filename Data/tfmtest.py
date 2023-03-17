import numpy as np
import PseudoTimeDomain as ptd
import os.path
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# use the total focusing method to find the responses in 3d space

# create a 3d meshgrid
x = np.linspace(-0.2, 0.2, 21)
y = np.linspace(-0.2, 0.2, 21)
z = np.linspace(0.01, 0.2, 20)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

dx = x[1]-x[0]
dy = y[1]-y[0]
dz = z[1]-z[0]

x_edges = np.append(x, x[-1]+dx)-dx/2
y_edges = np.append(y, y[-1]+dy)-dy/2
z_edges = np.append(z, z[-1]+dz)-dz/2
X_edges, Y_edges, Z_edges = np.meshgrid(
    x_edges, y_edges, z_edges, indexing='ij')

# create a PseudoTimeDomain object
pseudo_signal = ptd.PseudoTimeDomain(15, 20)


radui = range(5, 16, 5)
gain_time = []
# load data
for sensor_radius in radui:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "radius_"+str(sensor_radius)+".csv"))), newline='') as f:
        reader = csv.reader(f)
        gain_time_temp = list(reader)
    gain_time_2d = []
    for angle in gain_time_temp:
        gain_time_2d.append(
            [int(i.replace('[', '').replace(']', '')) for i in angle])
    gain_time.append(gain_time_2d)
sensor_angles = np.arange(0, 360, int(360/len(gain_time[0])))

# use the pseudo time domain object to find the responses using the gain time data
# important the [1]!!!!!!!!!!
pseudo_signal.positionPings2D(gain_time[1], 6000)

# 3d array of zeros to store the responses in the meshgrid
responses = np.zeros_like(X)

aperture_6db_angle = np.radians(72)

sensor_radius = 0.1

# loop through each distance in the pseudo time domain object and find the response at each point in the meshgrid
for t, response_t in enumerate(pseudo_signal.distance_responses):
    d = pseudo_signal.distance[t]/100
    # d = 0.2
    # response_t = [1]
    for angle, response_a in enumerate(response_t):
        radius_of_aperture = d*np.sin(aperture_6db_angle/2)
        sensor_position_x = sensor_radius * \
            np.sin(np.radians(sensor_angles[angle]))
        sensor_position_y = sensor_radius * \
            np.cos(np.radians(sensor_angles[angle]))

        distance_to_sensor_edges_sq = ((X_edges-sensor_position_x)**2 + (Y_edges-sensor_position_y)**2 + Z_edges**2)
        edges_before_d = distance_to_sensor_edges_sq < d**2
        edges_after_d = distance_to_sensor_edges_sq >= d**2
        cells_after_d = np.logical_or(edges_after_d[:-1, :-1, :-1], edges_after_d[1:, :-1, :-1])
        cells_after_d = np.logical_or(cells_after_d, edges_after_d[:-1, 1:, :-1])
        cells_after_d = np.logical_or(cells_after_d, edges_after_d[:-1, :-1, 1:])
        cells_after_d = np.logical_or(cells_after_d, edges_after_d[1:, 1:, :-1])
        cells_after_d = np.logical_or(cells_after_d, edges_after_d[1:, :-1, 1:])
        cells_after_d = np.logical_or(cells_after_d, edges_after_d[:-1, 1:, 1:])
        cells_after_d = np.logical_or(cells_after_d, edges_after_d[1:, 1:, 1:])

        cells_before_d = np.logical_or(edges_before_d[:-1, :-1, :-1], edges_before_d[1:, :-1, :-1])
        cells_before_d = np.logical_or(cells_before_d, edges_before_d[:-1, 1:, :-1])
        cells_before_d = np.logical_or(cells_before_d, edges_before_d[:-1, :-1, 1:])
        cells_before_d = np.logical_or(cells_before_d, edges_before_d[1:, 1:, :-1])
        cells_before_d = np.logical_or(cells_before_d, edges_before_d[1:, :-1, 1:])
        cells_before_d = np.logical_or(cells_before_d, edges_before_d[:-1, 1:, 1:])
        cells_before_d = np.logical_or(cells_before_d, edges_before_d[1:, 1:, 1:])

        cells_at_d = np.logical_and(cells_after_d, cells_before_d)

        # restrict the response within the radius of the aperture
        distance_to_centre_of_aperture = np.sqrt(
            (X-sensor_position_x)**2 + (Y-sensor_position_y)**2)
        cells_in_radius = np.logical_and(
            cells_at_d, distance_to_centre_of_aperture < radius_of_aperture)

        if radius_of_aperture == 0:
            power_scale = np.zeros_like(distance_to_centre_of_aperture)
        else:
            power_scale = distance_to_centre_of_aperture/radius_of_aperture
            power_scale[power_scale < 0] = 0
        responses[cells_at_d] += response_a*- \
            (((power_scale[cells_at_d])-4)**3)/64


to_plot_x = int(1*len(x)/2)
to_plot_y = int(1*len(y)/2)
to_plot_z = int(1*len(z)/2)

colour_scale = dict(cmin=0, cmax=np.max(responses))

X_plot, Y_plot = np.meshgrid(x, y)
Z_plot = np.ones_like(X_plot)*z[to_plot_z]
z_slice = go.Surface(x=X_plot, y=Y_plot, z=Z_plot,
                     surfacecolor=responses[:, :, to_plot_z].T, **colour_scale)

X_plot, Z_plot = np.meshgrid(x, z)
Y_plot = np.ones_like(X_plot)*y[to_plot_y]
y_slice = go.Surface(x=X_plot, y=Y_plot, z=Z_plot,
                     surfacecolor=responses[:, to_plot_y, :].T, **colour_scale)

Y_plot, Z_plot = np.meshgrid(y, z)
X_plot = np.ones_like(Y_plot)*x[to_plot_x]
x_slice = go.Surface(x=X_plot, y=Y_plot, z=Z_plot,
                     surfacecolor=responses[to_plot_x, :, :].T, **colour_scale)
fig1 = go.Figure(data=[x_slice, y_slice, z_slice])
fig1.update_layout(
    coloraxis=dict(colorscale='BrBG',
                   colorbar_thickness=25,
                   colorbar_len=0.75,
                   **colour_scale))
fig1.show()


# plot x, y and y slices of the responses in 2d using imshow on their own figures
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(responses[to_plot_x, :, :], extent=[
          z[0], z[-1], y[-1], y[0]], aspect='auto')
ax.set_title('x = ' + str(x[to_plot_x]))
ax.set_xlabel('z')
ax.set_ylabel('y')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(responses[:, to_plot_y, :], extent=[
          z[0], z[-1], x[-1], x[0]], aspect='auto')
ax.set_title('y = ' + str(y[to_plot_y]))
ax.set_xlabel('z')
ax.set_ylabel('x')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(responses[:, :, to_plot_z], extent=[
          y[0], y[-1], x[-1], x[0]], aspect='auto')
ax.set_title('z = ' + str(z[to_plot_z]))
ax.set_xlabel('y')
ax.set_ylabel('x')

# replace 0s with nans
responses[responses == 0] = np.nan
# plot the responses in 3d using scatter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z, c=responses)
plt.show()
