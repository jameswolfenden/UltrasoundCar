# model the time for an ultrasound pulse to travel from the transducer to a point in space and back for different transducer locations
import numpy as np
import pandas as pd
import os.path
from pathlib import Path
import matplotlib.pyplot as plt

# define the speed of sound in air
c = 343

# define the transducer locations
sensor_angles = np.linspace(0, 2*np.pi, 36, endpoint=False)
sensor_radius = 0.025
sensor_x = sensor_radius * -np.cos(sensor_angles)
sensor_y = sensor_radius * np.sin(sensor_angles)
sensor_z = 0.0

# define the point in space
point_x = 0.1
point_y = 0.1
point_z = 0.2

# print the point location
print("x: ", point_x, ", y: ", point_y, ", z: ", point_z)

# find the distance from the sensor to the point
sensor_point_distance = np.sqrt((sensor_x - point_x)**2 + (sensor_y - point_y)**2 + (sensor_z - point_z)**2)

# work out the time for the ultrasound pulse to travel from the transducer to the point and back
sensor_point_time = 2 * sensor_point_distance / c

# convert to microseconds
sensor_point_time = sensor_point_time * 1e6

# convert to integers
sensor_point_time = np.round(sensor_point_time).astype(int)

# save the results to a csv file
sensor_point_time_df = pd.DataFrame(sensor_point_time)
sensor_point_time_df.to_csv(os.path.join(Path(__file__).resolve().parents[1], os.path.join("Robot", os.path.join("UploadFolder", "sensor_point_time"+str(sensor_radius*100)+".csv"))), header=None, index=None)

# plot time against angle in degrees
plt.plot(sensor_angles * 180 / np.pi, sensor_point_time)
plt.xlabel("Angle (degrees)")
plt.ylabel("Time (microseconds)")
plt.show()