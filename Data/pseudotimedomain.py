# ultrasound data processing module
import numpy as np
import math
import scipy.signal as signal
from scipy.fft import ifft
from scipy.signal import find_peaks

# class
class PseudoTimeDomain:

    analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]

    # constructor, set the parameters for signal
    def __init__(self, cycles, points_per_cycle, frequency=0.04):
        self.cycles = cycles
        self.points_per_cycle = points_per_cycle
        self.ping_duration = cycles/frequency
        self.distance_time_scale = 1/frequency*343*10**-6/2  # 343m/s is the speed of sound and 10**6 is to convert to microseconds and 2 is to get the distance to the object
        self.frequency = frequency
        self.sample_frequency = frequency*points_per_cycle
        self.ifft_result = ifft([0,points_per_cycle,0], points_per_cycle)
        self.signal_result = np.tile(self.ifft_result,cycles)
        self.t = np.arange(cycles*points_per_cycle)
        self.window = signal.windows.hann(cycles*points_per_cycle)
        self.ping_shape = np.multiply(self.window,self.signal_result)

    def positionPings2D(self, gain_time, signal_duration):
        self.signal_duration = signal_duration
        self.gain_time = gain_time
        # Create the 2d array to store the signal
        self.signal_responses = np.zeros((int(self.signal_duration*self.sample_frequency),len(gain_time)),dtype=complex)
        # calculate the response at each distance
        for i_outer, outer in enumerate(gain_time):
            for i_ping, ping in enumerate(outer):
                if not (ping == 0 or ping >self.signal_duration-self.ping_duration/2): # make sure response is within the signal duration
                    self.signal_responses[int(ping*self.sample_frequency)-math.ceil(self.cycles*self.points_per_cycle/2):int(ping*self.sample_frequency)+int(self.cycles*self.points_per_cycle/2),i_outer] +=self.ping_shape*1/math.sqrt(self.analogue_gains[i_ping])
        self.distance_responses = np.abs(self.signal_responses)
        #self.distance_responses[ self.distance_responses==0 ] = np.nan # set 0 values to nan so they are not plotted
        self.distance = np.arange(0,(int(self.signal_duration*self.sample_frequency))*self.distance_time_scale,self.distance_time_scale)

    def positionPings3D(self, gain_time, signal_duration):
        self.signal_duration = signal_duration
        self.gain_time = gain_time
        # create 3d array to store signal
        self.signal_responses = np.zeros((int(self.signal_duration*self.sample_frequency),len(gain_time),len(gain_time[0])),dtype=complex)
        # calculate the response at each distance
        for i_outer, outer in enumerate(gain_time):
            for i_inner, inner in enumerate(outer):
                for i_ping, ping in enumerate(inner):
                    if not (ping == 0 or ping >self.signal_duration-self.ping_duration/2): # make sure response is within the signal duration
                        self.signal_responses[int(ping*self.sample_frequency)-math.ceil(self.cycles*self.points_per_cycle/2):int(ping*self.sample_frequency)+int(self.cycles*self.points_per_cycle/2),i_outer,i_inner] +=self.ping_shape*1/math.sqrt(self.analogue_gains[i_ping])
        self.distance_responses = np.abs(self.signal_responses)
        self.distance_responses[ self.distance_responses==0 ] = np.nan # set 0 values to nan so they are not plotted
        self.distance = np.arange(0,(int(self.signal_duration*self.sample_frequency))*self.distance_time_scale,self.distance_time_scale)

    def findxyz(self, scan_position, sensor_offset, radui):
        print("you havent done anything with the sensor offset yet")
        # convert angle and radius to x and y
        x = np.zeros((len(self.gain_time),len(self.gain_time[0])))
        z = np.zeros((len(self.gain_time),len(self.gain_time[0])))
        y = scan_position # scan being taken X m from sensor
        angles = np.arange(0,360, int(360/len(self.gain_time[0])))
        for i_radius, radius in enumerate(radui):
            for i_angle, angle in enumerate(angles):
                z[i_radius,i_angle] = math.cos(math.radians(angle))*radius
                x[i_radius,i_angle] = math.sin(math.radians(angle))*radius
        modulus = np.sqrt(x**2+y**2+z**2)
        x = np.multiply(x,1/modulus)
        y = np.multiply(y,1/modulus)
        z = np.multiply(z,1/modulus)
        return x,y,z

    def sphericalToCartesian(self, scan_position, sensor_offset, radui):
        x,y,z = self.findxyz(scan_position, sensor_offset, radui)
        # create a 3d array to store the distance in x,y,z for each angle and radius
        self.distance_x = np.zeros((len(self.distance),len(self.gain_time),len(self.gain_time[0])))
        self.distance_y = np.zeros((len(self.distance),len(self.gain_time),len(self.gain_time[0])))
        self.distance_z = np.zeros((len(self.distance),len(self.gain_time),len(self.gain_time[0])))
        angles = np.arange(0,360, int(360/len(self.gain_time[0])))
        for i_radius, radius in enumerate(radui):
            for i_angle, angle in enumerate(angles):
                self.distance_x[:,i_radius,i_angle] = self.distance*x[i_radius,i_angle]
                self.distance_y[:,i_radius,i_angle] = self.distance*y[i_radius,i_angle]
                self.distance_z[:,i_radius,i_angle] = self.distance*z[i_radius,i_angle]
    
    # use scipy to find peaks in the signal
    def findPeaks(self, response):
        peaks = signal.find_peaks(response)
        peak_heights = response[peaks[0]].tolist()
        peak_positions = peaks[0].tolist()
        return peak_heights, peak_positions
    
    def findPeaks2D(self,responses):
        peak_heights = []
        peak_positions = []
        for scan in responses.T:
            h,p = self.findPeaks(scan)
            peak_heights.append(h)
            peak_positions.append(p)
        return peak_heights, peak_positions
    
    def findPeaks3D(self, planes):
        peak_heights = []
        peak_positions = []
        for plane in np.moveaxis(planes,0,-1):
            h,p = self.findPeaks2D(plane.T)
            peak_heights.append(h)
            peak_positions.append(p)
        return peak_heights, peak_positions

    def cartesianPeaks(self, peak_positions, scan_position, sensor_offset, radui):
        # find the x,y,z of the peaks
        x,y,z = self.findxyz(scan_position, sensor_offset, radui)
        peak_x = []
        peak_y = []
        peak_z = []
        for plane, peak_plane in enumerate(peak_positions):
            peak_x_plane = []
            peak_y_plane = []
            peak_z_plane = []
            for scan, peak_scan in enumerate(peak_plane):
                peak_x_scan = []
                peak_y_scan = []
                peak_z_scan = []
                for i, peak in enumerate(peak_scan):
                    peak_x_scan.append(x[plane,scan]*peak*self.distance_time_scale)
                    peak_y_scan.append(y[plane,scan]*peak*self.distance_time_scale)
                    peak_z_scan.append(z[plane,scan]*peak*self.distance_time_scale)
                peak_x_plane.append(peak_x_scan)
                peak_y_plane.append(peak_y_scan)
                peak_z_plane.append(peak_z_scan)
            peak_x.append(peak_x_plane)
            peak_y.append(peak_y_plane)
            peak_z.append(peak_z_plane)
            
                    
        return peak_x, peak_y, peak_z
            