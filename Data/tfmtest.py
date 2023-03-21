import numpy as np
import PseudoTimeDomain as ptd
import os.path
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import scipy.io as sio
from scipy.interpolate import interp1d

# use the total focusing method to find the responses in 3d space

# create a 3d meshgrid
x = np.linspace(-0.25, 0.25, 51)
y = np.linspace(-0.25, 0.25, 51)
z = np.linspace(0.01, 0.5, 50)
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

pipe_radius = 150 * 1e-3


radui = [7.5]
gain_time = []
# load data
for sensor_radius in radui:
    with open(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "scan_data_time_8.1.csv"))), newline='') as f:
        reader = csv.reader(f)
        gain_time_temp = list(reader)
    gain_time_2d = []
    for angle in gain_time_temp:
        gain_time_2d.append(
            [int(i.replace('[', '').replace(']', '')) for i in angle])
    gain_time.append(gain_time_2d)
sensor_angles = np.arange(0, 360, int(360/len(gain_time[0])))-90  # start at 9 o'clock

# use the pseudo time domain object to find the responses using the gain time data
# important the [0]!!!!!!!!!!
# find largest value in gain_time[0]
max_gain_time = max([max(i) for i in gain_time[0]])

pseudo_signal.positionPings2D(gain_time[0], int(max_gain_time + pseudo_signal.ping_duration / 2 + 10))

print("Ping positions found")

# 3d array of zeros to store the responses in the meshgrid
responses = np.zeros_like(X, dtype=np.complex128)

aperture_6db_angle = np.radians(72)

sensor_radius = radui[0]/100

# iterate through each angle in the signal responses
for i, angle in enumerate(sensor_angles):
    sensor_position_x = sensor_radius * np.sin(np.radians(angle))
    sensor_position_y = sensor_radius * np.cos(np.radians(angle))
    distance_to_sensor = np.sqrt((X-sensor_position_x)**2 + (Y-sensor_position_y)**2 + Z**2)
    # interpolate the signal response to the delay
    interpolated_response_f = interp1d(pseudo_signal.distance, pseudo_signal.signal_responses[:,i], axis=0)
    interpolated_response = interpolated_response_f(distance_to_sensor)

    # apply the directivity function
    distance_to_centre_of_aperture = np.sqrt(
        (X-sensor_position_x)**2 + (Y-sensor_position_y)**2)
    angle_to_centre_of_aperture = np.sin(distance_to_centre_of_aperture/Z)
    power_scale = np.sin(1.5*angle_to_centre_of_aperture)/(1.5*angle_to_centre_of_aperture)
    responses += interpolated_response*power_scale


print("Loop complete")

# find the abs of the responses
responses = np.abs(responses)
responses[responses == 0] = 1e-10

# convert to dB
responses = 20*np.log10(responses/np.max(responses))

to_plot_x = int(1*len(x)/2)
to_plot_y = int(1*len(y)/2)
to_plot_z = int(1*len(z)/2)

colour_scale = dict(cmin=-25, cmax=np.max(responses), colorscale="Jet")

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

# plot the slices
fig1 = go.Figure(data=[x_slice, y_slice, z_slice])
fig1.update_layout(
    coloraxis=dict(colorbar_thickness=25,
                   colorbar_len=0.75,
                   **colour_scale))
fig1.show()


X_plot, Y_plot = np.meshgrid(x, y)
fig2 = go.Figure(
    frames=[go.Frame(
        data=[go.Surface(
            x=X_plot, y=Y_plot, z=np.ones_like(X_plot) * z[to_plot],
            surfacecolor=responses[:, :, to_plot].T, **colour_scale),
            x_slice, y_slice],
        name=str(to_plot)) for to_plot in range(len(z))])

# Add data to be displayed before animation starts
fig2.add_trace(go.Surface(x=X_plot, y=Y_plot, z=np.zeros_like(
    X_plot), surfacecolor=responses[:, :, 0].T, **colour_scale))
fig2.add_trace(x_slice)
fig2.add_trace(y_slice)


def frame_args(duration):
    return {
        "frame": {"duration": duration},
        "mode": "immediate",
        "fromcurrent": True,
        "transition": {"duration": duration, "easing": "linear"},
    }


sliders = [
    {
        "pad": {"b": 10, "t": 60},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [
            {
                "args": [[f.name], frame_args(0)],
                "label": str(to_plot),
                "method": "animate",
            }
            for to_plot, f in enumerate(fig2.frames)
        ],
    }
]

# Layout
fig2.update_layout(
    title='Slices in volumetric data',
    scene=dict(
        zaxis=dict(range=[np.min(z)-0.01, np.max(z)+0.01]),
    ),
    updatemenus=[
        {
            "buttons": [
                {
                    "args": [None, frame_args(50)],
                    "label": "&#9654;",  # play symbol
                    "method": "animate",
                },
                {
                    "args": [[None], frame_args(0)],
                    "label": "&#9724;",  # pause symbol
                    "method": "animate",
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 70},
            "type": "buttons",
            "x": 0.1,
            "y": 0,
        }
    ],
    sliders=sliders
)

fig2.show()

X_plot = Z.flatten() * 1e2
Y_plot = X.flatten() * 1e2
Z_plot = Y.flatten() * 1e2
value_plot = responses
value_plot[X**2 + Y**2 > (pipe_radius*1.1)**2] = -9999
value_plot = value_plot.flatten()


fig3 = go.Figure(data=go.Isosurface(
    x=X_plot,
    y=Y_plot,
    z=Z_plot,
    value=value_plot,
    isomin=-15,
    isomax=0,
    caps=dict(x_show=False, y_show=False),
    colorscale='jet',
    surface_count=6,
    opacity=0.3
    ))

# Plot Pipe Wall
pipe_theta = np.linspace(0, 2*np.pi, 100)
pipe_ang, Z_pipe = np.meshgrid(pipe_theta, z)
X_pipe = pipe_radius * np.cos(pipe_ang)
Y_pipe = pipe_radius * np.sin(pipe_ang)

pipe_color = [[0, 'red'],
             [1, 'red']]
fig3.add_trace(go.Surface(
   x = Z_pipe * 1e2,
   y = X_pipe * 1e2,
   z = Y_pipe * 1e2,
   colorscale = pipe_color,
   showscale=False,
   opacity=0.1
   ))

camera = dict(eye=dict(x=1.5, y=2.5, z=0.6))
fig3.update_layout(scene_camera = camera)
fig3.update_layout(scene_aspectmode='data')
fig3.update_layout(margin=dict(r=10, b=10, l=10, t=10))
fig3.update_layout(scene=dict(xaxis_title='Z (cm)', yaxis_title='X (cm)', zaxis_title='Y (cm)'),
                  font=dict(family="verdana", color="Black", size=18))
# fig3.update_layout(
#     width=2000,
#     height=2000,
# )
# fig3.write_image("fig3.svg")
fig3.show()



# save reponses to a mat file
sio.savemat('responses.mat', {'responses': responses})

plot_all = False
if (plot_all == True):
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
