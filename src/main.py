import numpy as np
from math import radians, pi
import matplotlib.pyplot as plt
from mayavi import mlab
from tvtk.api import tvtk # python wrappers for the C++ vtk ecosystem

# %% initialize Orekit : start up the java engine and expose the orekit classes in python.
import orekit
vm = orekit.initVM()
from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir()
from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.time import TimeScalesFactory, AbsoluteDate, DateComponents, TimeComponents
from org.orekit.utils import IERSConventions, Constants
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator

## Check Orekit installations
#print ('Java version:',vm.java_version)
#print ('Orekit version:', orekit.VERSION)
earth_radius = Constants.WGS84_EARTH_EQUATORIAL_RADIUS  # in kilometers


# %% import custom functions
from MATS_datareader import  MATS_TLEs_txt_file_parse
from other_functions import *


# %% Preprocessing MATS TLEs
MATS_TLEs_file_path = 'datafiles/sat000054227.txt'
lines = MATS_TLEs_txt_file_parse(MATS_TLEs_file_path)
num_rows = get_dimensions(lines)[0]
TLEs = []
for i in range(0, num_rows-1, 2):
    TLEs.append(TLE(lines[i],lines[i+1]))
    # TLEs is thus a list of 'org.orekit.propagation.analytical.tle.TLE' objects

# shortening TLE list for initial trials, updating num_rows
TLEs = TLEs[1:50]
num_rows = len(TLEs)*2





# %% Preparing Co-ordinate system
ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ITRF)

# %% Define the Station
longitude = radians(21.063)
latitude  = radians(67.878)
altitude  = 341.0
station = GeodeticPoint(latitude, longitude, altitude)
station_frame = TopocentricFrame(earth, station, "Esrange")
inertialFrame = FramesFactory.getEME2000()

el=[]
pos=[]

# %% Propagating different TLEs
# from TLE_epoch_01 to TLE_epoch_02, we consider TLE_01,
# from TLE_epoch_02 to TLE_epoch_03, we consider TLE_02,
# and so on..

for j in range(0, (num_rows//2)-1, 1):

    current_TLE = TLEs[j]
    next_TLE = TLEs[j+1]

    extrapDate = current_TLE.getDate()
    finalDate = next_TLE.getDate() #seconds

    propagator = TLEPropagator.selectExtrapolator(current_TLE)

    # %% Performing Propagation in steps of 10 seconds from extrapDate to finalDate
    while (extrapDate.compareTo(finalDate) <= 0.0):
        pv = propagator.getPVCoordinates(extrapDate, inertialFrame)
        pos_tmp = pv.getPosition()
        pos.append((pos_tmp.getX(),pos_tmp.getY(),pos_tmp.getZ()))

        el_tmp = station_frame.getElevation(pv.getPosition(),inertialFrame,extrapDate)*180.0/pi
        el.append(el_tmp)
        #print extrapDate, pos_tmp, vel_tmp
        extrapDate = extrapDate.shiftedBy(10.0)

#Constants.WGS84_EARTH_EQUATORIAL_RADIUS

'''
# %% Plot Results
plt.plot(el)
plt.ylim(0,90)
plt.title('Elevation')
plt.grid(True)
plt.show()
'''





# Create a new Mayavi figure
fig = mlab.figure()

# %% Plot the Earth surface
image_file = 'datafiles/blue_marble.jpg'
# load and map the texture
img = tvtk.JPEGReader()
img.file_name = image_file
texture = tvtk.Texture(input_connection=img.output_port, interpolate=1)
# (interpolate for a less raster appearance when zoomed in)
# use a TexturedSphereSource, a.k.a. getting our hands dirty
Nrad = 180
# create the sphere source with a given radius and angular resolution
sphere = tvtk.TexturedSphereSource(radius = earth_radius, theta_resolution=Nrad, phi_resolution=Nrad)
# assemble rest of the pipeline, assign texture
sphere_mapper = tvtk.PolyDataMapper(input_connection=sphere.output_port)
sphere_actor = tvtk.Actor(mapper=sphere_mapper, texture=texture)
fig.scene.add_actor(sphere_actor)

# %% Plot the orbit
# extract position data
x_orbit = [point[0] for point in pos]
y_orbit = [point[1] for point in pos]
z_orbit = [point[2] for point in pos]

# Generate scalar values for each point on the line
scalar_values = np.linspace(0, 1, len(x_orbit))  # Example: Linearly varying scalar values from 0 to 1

line = mlab.plot3d(x_orbit, y_orbit, z_orbit, color = (1,0,0), tube_radius = None)

# Add a colorbar to the plot
#colorbar = mlab.colorbar()


# Display the plot
mlab.show()
