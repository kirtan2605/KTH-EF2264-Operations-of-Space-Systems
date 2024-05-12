import os

import numpy as np
from math import radians, pi, floor
import matplotlib.pyplot as plt
<<<<<<< HEAD
=======
#from mayavi import mlab
#from tvtk.api import tvtk # python wrappers for the C++ vtk ecosystem
>>>>>>> 6e5fde965cd1811010b33ae519820ea5ceb169db

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
from other_functions import *

def get_TLEfilepaths_in_folder(folder_path):
    filenames = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            filenames.append(folder_path+"/"+filename)
    return filenames

def absolutedate_to_datetime(orekit_absolutedate):
    ''' Converts between orekit.AbsoluteDate objects
    and python datetime objects (utc)'''

    utc = TimeScalesFactory.getUTC()
    or_comp = orekit_absolutedate.getComponents(utc)
    or_date = or_comp.getDate()
    or_time = or_comp.getTime()
    seconds = or_time.getSecond()
    # returns string YYYY-MM-DD_HH:MM:SS
    return f"{str(or_date.getYear())}-{str(or_date.getMonth())}-{str(or_date.getDay())}T{str(or_time.getHour())}:{str(or_time.getMinute())}:{str(int(floor(seconds)))}"

def create_absolute_date(inputDate):
    # Set up time scales and IERS conventions
    year, month, day, hour, minute, second = inputDate
    # Create AbsoluteDate object
    absolute_date = AbsoluteDate(year, month, day, hour, minute, second, TimeScalesFactory.getUTC())

    return absolute_date

def propagate_TLE(TLE_filepath, timeStep):

    pos = np.empty((array_length, 3))   # 3 since, the X,Y,Z co-ordinates are being stored

    lines = txt_file_parse(TLE_filepath)
    num_rows = get_dimensions(lines)[0]
    TLEs = []
    for i in range(0, num_rows-1, 2):
        TLEs.append(TLE(lines[i],lines[i+1]))
        # TLEs is thus a list of 'org.orekit.propagation.analytical.tle.TLE' objects

    # %% Preparing Co-ordinate system
    inertialFrame = FramesFactory.getEME2000()
    print(f'Starlink Satellite being parsed : {StarlinkSat_count} of {total_Starlink}')

    # %% Propagating different TLEs
    # from TLE_epoch_01 to TLE_epoch_02, we consider TLE_01,
    # from TLE_epoch_02 to TLE_epoch_03, we consider TLE_02,
    # and so on..

    time_counter = 0
    TLE_counter = 0
    iterDate = beginAbsoluteDate

    for TLE_counter in range(len(TLEs)-1):

        current_TLE = TLEs[TLE_counter]
        next_TLE = TLEs[TLE_counter+1]

        lowerDate = current_TLE.getDate()
        upperDate = next_TLE.getDate() #seconds

        while (iterDate.compareTo(lowerDate) >= 0.0)&(iterDate.compareTo(upperDate) < 0.0)&(iterDate.compareTo(endAbsoluteDate) <= 0.0) :
            propagator = TLEPropagator.selectExtrapolator(current_TLE)

            # %% Performing Propagation in steps of 10 seconds from extrapDate to finalDate
            pv = propagator.getPVCoordinates(iterDate, inertialFrame)
            pos_tmp = pv.getPosition()
            pos[time_counter,:] = [pos_tmp.getX(),pos_tmp.getY(),pos_tmp.getZ()]
            #print(pos)
            #print(iterDate)

            iterDate = iterDate.shiftedBy(timeStep)
            time_counter = time_counter + 1


    return pos

# %% Preprocessing MATS TLEs
MATS_TLEs_file_path = "datafiles/54227.txt"
StarlinkData_folder_path = "datafiles/StarlinkData-2023"
Starlink_TLEs_file_path = get_TLEfilepaths_in_folder(StarlinkData_folder_path)

global StarlinkSat_count
global total_Starlink
total_Starlink = len(Starlink_TLEs_file_path)
StarlinkSat_count = 0




# %% SECTION 1 : Propagate TLEs

date=[]     # Check if still required

global array_length
global beginAbsoluteDate
global endAbsoluteDate

# %% Defining Dates of interest
beginDate = (2023, 1, 1, 0, 0, 0.0)   # 1 January 2023, 00:00:00
endDate = (2023, 1, 31, 0, 0, 0.0)     # 31 January 2023, 00:00:00
beginAbsoluteDate = create_absolute_date(beginDate)
endAbsoluteDate = create_absolute_date(endDate)
seconds_diff = endAbsoluteDate.durationFrom(beginAbsoluteDate)

# IMPORTANT!!! Use float to specify propagation step in seconds
propagationStep_seconds = 60.0

array_length = int(seconds_diff/propagationStep_seconds) + 1

print(beginAbsoluteDate)
print(endAbsoluteDate)

np.savetxt(f'datafiles/SatellitePositions-NumpyArray/MATS.txt', propagate_TLE(MATS_TLEs_file_path, propagationStep_seconds))

Starlink_pos_counter = 0
for path in Starlink_TLEs_file_path:
    StarlinkSat_count = StarlinkSat_count + 1
    Starlink_pos_counter = Starlink_pos_counter + 1
    np.savetxt(f'datafiles/SatellitePositions-NumpyArray/Starlink_{str(Starlink_pos_counter).zfill(3)}.txt', propagate_TLE(path, propagationStep_seconds))
print("Executed Successfully")



#Constants.WGS84_EARTH_EQUATORIAL_RADIUS
