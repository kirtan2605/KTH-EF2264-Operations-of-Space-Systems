
from math import radians, pi
import matplotlib.pyplot as plt

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
#print (Constants.WGS84_EARTH_EQUATORIAL_RADIUS)


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






# %% Setting up the TLEs

#SPOT-5
tle_line1 = "1 27421U 02021A   02124.48976499 -.00021470  00000-0 -89879-2 0    20"
tle_line2 = "2 27421  98.7490 199.5121 0001333 133.9522 226.1918 14.26113993    62"

mytle = TLE(tle_line1,tle_line2)

print (mytle)
print ('Epoch :',mytle.getDate())

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

    # Set the start and end date that is then used for the propagation in seconds
    #extrapDate = AbsoluteDate(2002, 5, 7, 12, 0, 0.0, TimeScalesFactory.getUTC())
    #finalDate = extrapDate.shiftedBy(60.0*60*24) #seconds
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


# %% Plot Results
plt.plot(el)
plt.ylim(0,90)
plt.title('Elevation')
plt.grid(True)
plt.show()
