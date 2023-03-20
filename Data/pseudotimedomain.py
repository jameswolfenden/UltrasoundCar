# ultrasound data processing module
import numpy as np
import math
import scipy.signal as signal
from scipy.fft import ifft
from scipy.signal import find_peaks
from scipy.interpolate import griddata

# class
class PseudoTimeDomain:

    analogue_gains = [40, 50, 60, 70,80, 100, 120, 140, 200, 250, 300, 350, 400, 500, 600, 700]
    other_gains = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]

    # constructor, set the parameters for signal
    def __init__(self, cycles, points_per_cycle, frequency=0.04, srf=True):
        self.cycles = cycles
        self.points_per_cycle = points_per_cycle
        self.ping_duration = cycles/frequency
        self.distance_time_scale = 1/(frequency*points_per_cycle)*343*(10**-6)/2  # 343m/s is the speed of sound and 10**6 is to convert to microseconds and 2 is to get the distance to the object
        self.distance_from_μs = 343*(10**-6)/2 # 343m/s is the speed of sound and 10**6 is to convert to microseconds and 2 is to get the distance to the object
        self.frequency = frequency
        self.sample_frequency = frequency*points_per_cycle
        self.ifft_result = ifft([0,points_per_cycle,0], points_per_cycle)
        self.signal_result = np.tile(self.ifft_result,cycles)
        self.t = np.arange(cycles*points_per_cycle)
        self.window = signal.windows.hann(cycles*points_per_cycle)
        self.ping_shape = np.multiply(self.window,self.signal_result)
        self.srf = srf
        if (srf==False):
            self.analogue_gains = self.other_gains

    def positionPings2D(self, gain_time, signal_end):
        self.signal_end = signal_end
        self.gain_time = gain_time
        # Create the 2d array to store the signal
        self.signal_responses = np.zeros((int((self.signal_end)*self.sample_frequency),len(gain_time)),dtype=complex)
        # calculate the response at each distance
        for i_outer, outer in enumerate(gain_time):
            for i_ping, ping in enumerate(outer):
                if not (ping == 0 or ping >self.signal_end-self.ping_duration/2): # make sure response is within the signal duration
                    if (self.srf==True):
                        self.signal_responses[int((ping)*self.sample_frequency)-math.ceil(self.cycles*self.points_per_cycle/2):int((ping)*self.sample_frequency)+int(self.cycles*self.points_per_cycle/2),i_outer] +=self.ping_shape*math.pow(self.analogue_gains[i_ping],-1.75)
                    else:
                        self.signal_responses[int(ping*self.sample_frequency)-math.ceil(self.cycles*self.points_per_cycle/2):int(ping*self.sample_frequency)+int(self.cycles*self.points_per_cycle/2),i_outer] +=self.ping_shape*1
        # normalise the signal to the maximum value
        self.signal_responses = self.signal_responses/np.max(self.signal_responses)
        self.distance_responses = np.abs(self.signal_responses)
        #self.distance_responses[ self.distance_responses==0 ] = np.nan # set 0 values to nan so they are not plotted
        self.distance = (np.arange(0, self.signal_responses.shape[0])/self.sample_frequency)*self.distance_from_μs

    def positionPings3D(self, gain_time, signal_end):
        self.signal_end = signal_end
        self.gain_time = gain_time
        # create 3d array to store signal
        self.signal_responses = np.zeros((int(self.signal_end*self.sample_frequency),len(gain_time),len(gain_time[0])),dtype=complex)
        # calculate the response at each distance
        for i_outer, outer in enumerate(gain_time):
            for i_inner, inner in enumerate(outer):
                for i_ping, ping in enumerate(inner):
                    if not (ping == 0 or ping >self.signal_end-self.ping_duration/2): # make sure response is within the signal duration
                        self.signal_responses[int(ping*self.sample_frequency)-math.ceil(self.cycles*self.points_per_cycle/2):int(ping*self.sample_frequency)+int(self.cycles*self.points_per_cycle/2),i_outer,i_inner] +=self.ping_shape*math.pow(self.analogue_gains[i_ping],-1.75)
        # normalise the signal to the maximum value
        self.signal_responses = self.signal_responses/np.max(self.signal_responses)
        self.distance_responses = np.abs(self.signal_responses)
        self.distance_responses[ self.distance_responses==0 ] = np.nan # set 0 values to nan so they are not plotted
        self.distance = np.arange(0,(int(self.signal_end*self.sample_frequency))*self.distance_time_scale,self.distance_time_scale)

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

    # find the response amplitude on a 3d grid
    def findResponseAmplitude3D(self, scan_position, sensor_offset, radui):
        angles = np.arange(0,360, int(360/len(self.gain_time[0])))
        # convert the distance responses to cartesian coordinates
        try: 
            self.distance_x
        except AttributeError:
            self.sphericalToCartesian(scan_position, sensor_offset, radui)
        # create x,y,z arrays to interpolate to
        self.xi = np.linspace(np.min(self.distance_x),np.max(self.distance_x),10)
        self.yi = np.linspace(np.min(self.distance_y),np.max(self.distance_y),10)
        self.zi = np.linspace(np.min(self.distance_z),np.max(self.distance_z),10)
        print("this doesnt actually do any interpolation yet but idk what i could do? also the loop is pointless i think?? does something anyway")
        # create a 3d array to store the response amplitude at each point in the 3d grid
        self.response_amplitude = np.zeros((len(self.xi),len(self.yi),len(self.zi)))
        # loop through each point in the 3d grid
        for i_x, x in enumerate(self.xi):
            for i_y, y in enumerate(self.yi):
                for i_z, z in enumerate(self.zi):
                    # loop through each angle and radius
                    for i_radius, radius in enumerate(radui):
                        for i_angle, angle in enumerate(angles):
                            # interpolate the distance response to the 3d grid point
                            # find points on the distance response that are within 1/2 the distance between points in the 3d grid in x,y,z
                            points = np.where((self.distance_x[:,i_radius,i_angle] < x+np.mean(np.diff(self.xi))/2) & (self.distance_x[:,i_radius,i_angle] > x-np.mean(np.diff(self.xi))/2) & (self.distance_y[:,i_radius,i_angle] < y+np.mean(np.diff(self.yi))/2) & (self.distance_y[:,i_radius,i_angle] > y-np.mean(np.diff(self.yi))/2) & (self.distance_z[:,i_radius,i_angle] < z+np.mean(np.diff(self.zi))/2) & (self.distance_z[:,i_radius,i_angle] > z-np.mean(np.diff(self.zi))/2))
                            # if there are points within 1/2 the distance between points in the 3d grid in x,y,z
                            if len(points[0]) > 0:
                                # find the distance response at the closest point
                                self.response_amplitude[i_x,i_y,i_z] += self.distance_responses[points[0][0],i_radius,i_angle]
                            # if there are no points within 1/2 the distance between points in the 3d grid in x,y,z do nothing

    # interpolate the distance responses to a 3d grid using griddata
    def interpolate3D(self, scan_position, sensor_offset, radui):
        # convert the distance responses to cartesian coordinates
        try: 
            self.distance_x
        except AttributeError:
            self.sphericalToCartesian(scan_position, sensor_offset, radui)
        # create x,y,z arrays to interpolate to
        self.xi = np.linspace(np.min(self.distance_x),np.max(self.distance_x),25)
        self.yi = np.linspace(np.min(self.distance_y),np.max(self.distance_y),25)
        self.zi = np.linspace(np.min(self.distance_z),np.max(self.distance_z),25)
        # interpolate the distance_x, distance_y, distance_z and distance_responses to a 3d grid
        self.interpolated_responses = griddata((self.distance_x.flatten(),self.distance_y.flatten(),self.distance_z.flatten()),self.distance_responses.flatten(),(self.xi[None,None,:],self.yi[None,:,None],self.zi[:,None,None]),method='nearest')
        
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