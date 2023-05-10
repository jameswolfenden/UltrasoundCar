import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import CubicSpline
from scipy.signal import hilbert
import matplotlib.pyplot as plt


def find_saft(x, y, z, sensor_radii, sensor_angles, time_domain_data, time_data, hilberted):
    dx = x[1]-x[0]
    dy = y[1]-y[0]
    dz = z[1]-z[0]
    # create a 3d meshgrid
    X, Y, Z = np.meshgrid(x+dx/2, y+dy/2, z+dz/2, indexing='ij')
    # 3d array of zeros to store the responses in the meshgrid
    responses = np.zeros_like(X, dtype=np.complex128)

    if not hilberted:
        time_domain_data = hilbert(time_domain_data)

    # iterate through each sensor radius
    for rad_i, sensor_radius in enumerate(sensor_radii):
        # iterate through each angle in the signal responses
        for i, angle in enumerate(sensor_angles):
            sensor_position_x = sensor_radius * np.sin(np.radians(angle))
            sensor_position_y = sensor_radius * np.cos(np.radians(angle))
            distance_to_sensor = np.sqrt((X-sensor_position_x)**2 + (Y-sensor_position_y)**2 + (Z)**2)
            # interpolate the signal response to the delay
            interpolated_response_f = CubicSpline(time_data, time_domain_data[rad_i, :, i], axis=0)
            interpolated_response = interpolated_response_f(distance_to_sensor)

            # apply the directivity function
            distance_to_centre_of_aperture = np.sqrt(
                (X-sensor_position_x)**2 + (Y-sensor_position_y)**2)
            angle_to_centre_of_aperture = np.arctan2(distance_to_centre_of_aperture, Z)
            # size of transducer and wavelength are hardcoded
            d = 0.0088
            wavelength = 0.008575
            power_scale = np.sin(np.pi*d/wavelength*np.sin(angle_to_centre_of_aperture)
                                 )/(np.pi*d/wavelength*np.sin(angle_to_centre_of_aperture))
            power_scale[power_scale <= 0] = 0.00001
            responses += interpolated_response#/(power_scale**0.1)
    return responses


def plot_sinc_function():
    d = 0.0088
    wavelength = 0.008575
    # polar plot of the sinc function
    theta = np.concatenate((np.linspace(0.001, np.pi/2, 100), np.linspace(3*np.pi/2, 2*np.pi, 100)))
    r = np.sin(np.pi*d/wavelength*np.sin(theta))/(np.pi*d/wavelength*np.sin(theta))
    #r[r < 0] = 0
    #r = r**0.5
    # plot polar with matplotlib
    fig = plt.figure(figsize=(3, 3))
    ax = fig.add_subplot(111, projection='polar')
    # get decibels
    r_dB = 20*np.log10(r/np.max(r))
    print(r)
    print(r_dB)
    ax.plot(theta, r_dB, 'r', linewidth=2)
    ax.grid(True)
    # set grid
    ax.set_rgrids(np.arange(-30, 0, 6), angle=0)
    ax.set_thetagrids(np.arange(0, 360, 30))
    ax.set_rlim(-30, 0)
    # set 0 to be at the top
    ax.set_theta_zero_location('N')
    # change the direction of the angle
    ax.set_theta_direction(-1)
    plt.savefig('sinc.svg')
    plt.show()

    # plot not polar with matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(theta, r)
    ax.grid(True)
    plt.show()


def convert_to_db(responses, *args):
    # find the abs of the responses
    responses = np.abs(responses)
    responses[responses == 0] = 1e-10
    # convert to db
    if len(args) == 0:
        responses = 20*np.log10(responses/np.max(responses))
    else:
        responses = 20*np.log10(responses/args[0])
    return responses


def plot_slices(responses, x, y, z, to_plot_x, to_plot_y, to_plot_z):
    colour_scale = dict(cmin=-25, cmax=np.max(responses), colorscale="Jet")

    X_plot, Y_plot = np.meshgrid(x, y)
    Z_plot = np.ones_like(X_plot)*z[to_plot_z]
    z_slice = go.Surface(x=Z_plot*100, y=X_plot*100, z=Y_plot*100,
                         surfacecolor=responses[:, :, to_plot_z].T, **colour_scale)

    X_plot, Z_plot = np.meshgrid(x, z)
    Y_plot = np.ones_like(X_plot)*y[to_plot_y]
    y_slice = go.Surface(x=Z_plot*100, y=X_plot*100, z=Y_plot*100,
                         surfacecolor=responses[:, to_plot_y, :].T, **colour_scale)

    Y_plot, Z_plot = np.meshgrid(y, z)
    X_plot = np.ones_like(Y_plot)*x[to_plot_x]
    x_slice = go.Surface(x=Z_plot*100, y=X_plot*100, z=Y_plot*100,
                         surfacecolor=responses[to_plot_x, :, :].T, **colour_scale)

    # plot the slices
    fig1 = go.Figure(data=[x_slice, y_slice, z_slice])
    fig1.update_layout(
        coloraxis=dict(colorbar_thickness=25,
                       colorbar_len=0.75,
                       **colour_scale),
        scene=dict(xaxis_title='z (cm)', yaxis_title='x (cm)', zaxis_title='y (cm)', xaxis=dict(autorange='reversed')),
        font=dict(family="verdana", color="Black", size=16))
    fig1.show()

    X_plot, Y_plot = np.meshgrid(x, y)
    fig2 = go.Figure(
        frames=[go.Frame(
            data=[go.Surface(
                y=X_plot*100, z=Y_plot*100, x=np.ones_like(X_plot)*100 * z[to_plot],
                surfacecolor=responses[:, :, to_plot].T, **colour_scale),
                x_slice, y_slice],
            name=str(to_plot)) for to_plot in range(len(z))])

    # Add data to be displayed before animation starts
    fig2.add_trace(go.Surface(y=X_plot*100, z=Y_plot*100, x=np.zeros_like(
        X_plot)*100, surfacecolor=responses[:, :, 0].T, **colour_scale))
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
        scene=dict(xaxis_title='z (cm)', yaxis_title='x (cm)', zaxis_title='y (cm)',
                   xaxis=dict(autorange='reversed')),
        font=dict(family="verdana", color="Black", size=16),
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


def plot_isosurface(responses, x, y, z, pipe_radius, isomin=-10, big=False):
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    X_plot = Z.flatten() * 1e2
    Y_plot = X.flatten() * 1e2
    Z_plot = Y.flatten() * 1e2
    value_plot = responses
    value_plot[X**2 + Y**2 > (pipe_radius*1.05)**2] = -9999  # remove values outside pipe
    value_plot = value_plot.flatten()

    isosrfce = go.Isosurface(
        x=X_plot,
        y=Y_plot,
        z=Z_plot,
        value=value_plot,
        isomin=isomin,
        isomax=0,
        caps=dict(x_show=False, y_show=False),
        colorscale='jet',
        surface_count=10,
        opacity=0.3
    )

    # Plot Pipe Wall
    pipe_theta = np.linspace(0, 2*np.pi, 100)
    pipe_ang, Z_pipe = np.meshgrid(pipe_theta, z)
    X_pipe = pipe_radius * np.cos(pipe_ang)
    Y_pipe = pipe_radius * np.sin(pipe_ang)

    pipe_color = [[0, 'red'],
                  [1, 'red']]
    srfc = go.Surface(
        x=Z_pipe * 1e2,
        y=X_pipe * 1e2,
        z=Y_pipe * 1e2,
        colorscale=pipe_color,
        showscale=False,
        opacity=0.1
    )

    x0 = 20  # z
    y0 = -5  # x
    z0 = -2  # y
    x1 = 26
    y1 = 5
    z1 = -12

    vertices = np.array([
        [x0, y0, z0],  # vertex 0
        [x1, y0, z0],  # vertex 1
        [x1, y0, z1],  # vertex 2
        [x0, y0, z1],  # vertex 3
        [x0, y1, z0],  # vertex 4
        [x1, y1, z0],  # vertex 5
        [x1, y1, z1],  # vertex 6
        [x0, y1, z1],  # vertex 7
    ])

    # define the faces of the box
    faces = np.array([
        [0, 1, 2],  # face 0
        [0, 2, 3],  # face 1
        [1, 5, 6],  # face 2
        [1, 6, 2],  # face 3
        [5, 4, 7],  # face 4
        [5, 7, 6],  # face 5
        [4, 0, 3],  # face 6
        [4, 3, 7],  # face 7
        [3, 2, 6],  # face 8
        [3, 6, 7],  # face 9
        [4, 5, 1],  # face 10
        [4, 1, 0],  # face 11
    ])

    box = go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        color='rgba(128, 128, 128, 0.2)',
    )
    z_pipe = 0
    circle_pipe = go.Scatter3d(
        y=pipe_radius*100 * np.cos(pipe_theta),
        z=pipe_radius*100 * np.sin(pipe_theta),
        x=z_pipe * np.ones_like(pipe_theta),
        mode='lines',
        line=dict(color='red', width=2),
        showlegend=False
    )
    fig3 = go.Figure(data=[isosrfce, srfc])
    if big:
#        camera = dict(eye=dict(x=2.6, y=-1.5, z=2), center=dict(x=0, y=0.2, z=-0.8))
#        fig3.update_layout(
#            width=900,
#            height=700,
#        )
        camera = dict(eye=dict(x=1, y=-1, z=0.6594586144012361), center=dict(x=-0.05, y=0, z=0), projection=dict(type='orthographic'))
        fig3.update_layout(
            width=900,
            height=500,
        )
        fig3.update_layout(
            scene=dict(
                xaxis_title='z (cm)', yaxis_title='x (cm)', zaxis_title='y (cm)',
                xaxis=dict(autorange='reversed',tick0=0, dtick=10)),
            font=dict(family="CMU Serif", color="Black", size=12))
        scale = 118
    else:
        #camera = dict(eye=dict(x=1.25, y=-1.25, z=1.25), center=dict(x=0, y=0, z=-0.25))
        #camera = dict(eye=dict(x=1, y=0, z=0), center=dict(x=0, y=0, z=0), projection=dict(type='orthographic'))
        camera = dict(eye=dict(x=1, y=-1, z=1), center=dict(x=0, y=0, z=0), projection=dict(type='orthographic'))
        #fig3.update_layout(
        #    width=350,
        #    height=300,
        #)
        fig3.update_layout(
            width=500,
            height=400,
        )
        fig3.update_layout(
            scene=dict(
                xaxis_title='z (cm)', yaxis_title='x (cm)', zaxis_title='y (cm)',
                #xaxis_showticklabels=False,
                xaxis=dict(autorange='reversed')),
            font=dict(family="CMU Serif", color="Black", size=12))
        scale =45
        scale = 69

    fig3.update_layout(scene_camera=camera)
    #fig3.update_layout(scene_aspectmode='data')
    fig3.update_layout(scene_aspectmode='manual', scene_aspectratio=dict(x=len(z)/scale, y=len(y)/scale, z=len(x)/scale))
    fig3.update_layout(margin=dict(r=0, b=0, l=0, t=0))
    fig3.write_image("fig3.svg")
    fig3.show(config = {'toImageButtonOptions': {'format': 'svg', 'filename': 'fig3New', 'height': 700, 'width': 900, 'scale': 1}})
