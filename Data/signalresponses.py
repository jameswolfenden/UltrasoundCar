import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import interp1d
from scipy.signal import hilbert
import matplotlib.pyplot as plt

def find_saft(x,y,z, sensor_radii, sensor_angles, time_domain_data, time_data, hilberted):
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
            interpolated_response_f = interp1d(time_data, time_domain_data[rad_i,:,i], axis=0)
            interpolated_response = interpolated_response_f(distance_to_sensor)

            # apply the directivity function
            distance_to_centre_of_aperture = np.sqrt(
                (X-sensor_position_x)**2 + (Y-sensor_position_y)**2)
            angle_to_centre_of_aperture = np.sin(distance_to_centre_of_aperture/Z)
            # size of transducer and wavelength are hardcoded
            power_scale = np.sin(np.pi*0.0088/0.008575*np.sin(angle_to_centre_of_aperture))/(np.pi*0.0088/0.008575*np.sin(angle_to_centre_of_aperture))
            power_scale[power_scale<0] = 0
            power_scale[distance_to_centre_of_aperture/Z>np.pi/2] = 0
            responses += interpolated_response*power_scale
    return responses

def plot_sinc_function():
    # polar plot of the sinc function
    theta = np.linspace(0, 2*np.pi, 1000)
    r = np.sin(np.pi*0.0088/0.008575*np.sin(theta))/(np.pi*0.0088/0.008575*np.sin(theta))
    # plot polar with matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.plot(theta, r)
    ax.grid(True)
    plt.show()

    # plot not polar with matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(theta, r)
    ax.grid(True)
    plt.show()


def convert_to_db(responses):
    # find the abs of the responses
    responses = np.abs(responses)
    responses[responses == 0] = 1e-10
    # convert to db
    responses = 20*np.log10(responses/np.max(responses))
    return responses

def plot_slices(responses, x, y, z, to_plot_x, to_plot_y, to_plot_z):
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

def plot_isosurface(responses, x, y, z, pipe_radius):
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
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
        isomin=-10,
        isomax=0,
        caps=dict(x_show=False, y_show=False),
        colorscale='jet',
        surface_count=10,
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


