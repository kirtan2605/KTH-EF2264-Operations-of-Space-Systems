
from math import radians, pi
import matplotlib.pyplot as plt

# %% initialize Orekit : start up the java engine and expose the orekit classes in python.
import orekit
vm = orekit.initVM()
#print ('Java version:',vm.java_version)
#print ('Orekit version:', orekit.VERSION)

from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir()

# orekit-data repository has been downloaded directly via pip
from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.time import TimeScalesFactory, AbsoluteDate, DateComponents, TimeComponents
from org.orekit.utils import IERSConventions, Constants

#print (Constants.WGS84_EARTH_EQUATORIAL_RADIUS)

from org.orekit.propagation.analytical.tle import TLE, TLEPropagator




# %% Setting up the TLEs

#tle_line_1 = '1 41999U 17008BD  21322.49427166  .00005929  00000-0  19476-3 0  9992'
#tle_line_2 = '2 41999  97.3103  30.0492 0005406 261.3283  98.7346 15.31932939264278'

#SPOT-5
tle_line1 = "1 27421U 02021A   02124.48976499 -.00021470  00000-0 -89879-2 0    20"
tle_line2 = "2 27421  98.7490 199.5121 0001333 133.9522 226.1918 14.26113993    62"

mytle = TLE(tle_line1,tle_line2)

print (mytle)
print ('Epoch :',mytle.getDate())

# %% Preparing Co-ordinate system
ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,Constants.WGS84_EARTH_FLATTENING, ITRF)

# %% Define the Station
longitude = radians(21.063)
latitude  = radians(67.878)
altitude  = 341.0
station = GeodeticPoint(latitude, longitude, altitude)
station_frame = TopocentricFrame(earth, station, "Esrange")

inertialFrame = FramesFactory.getEME2000()
propagator = TLEPropagator.selectExtrapolator(mytle)

# Set the start and end date that is then used for the propagation.
extrapDate = AbsoluteDate(2002, 5, 7, 12, 0, 0.0, TimeScalesFactory.getUTC())
finalDate = extrapDate.shiftedBy(60.0*60*24) #seconds

el=[]
pos=[]


# %% Performing Propagation
while (extrapDate.compareTo(finalDate) <= 0.0):
    pv = propagator.getPVCoordinates(extrapDate, inertialFrame)
    pos_tmp = pv.getPosition()
    pos.append((pos_tmp.getX(),pos_tmp.getY(),pos_tmp.getZ()))

    el_tmp = station_frame.getElevation(pv.getPosition(),inertialFrame,extrapDate)*180.0/pi
    el.append(el_tmp)
    #print extrapDate, pos_tmp, vel_tmp
    extrapDate = extrapDate.shiftedBy(10.0)

# %% Plot Results
plt.plot(el)
plt.ylim(0,90)
plt.title('Elevation')
plt.grid(True)
plt.show()
