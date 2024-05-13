import os
import numpy as np
import math

# %% initialize Orekit : start up the java engine and expose the orekit classes in python.
import orekit
vm = orekit.initVM()
from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir()
from org.orekit.utils import Constants

def get_Positions_filepaths_in_folder(folder_path):
    filenames = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            filenames.append(folder_path+"/"+filename)
    return filenames


def row_magnitudes(arr):
    """
    Calculate the magnitude of each row of a NumPy array.

    Parameters:
        arr (numpy.ndarray): Input array.

    Returns:
        numpy.ndarray: Array containing magnitudes of each row.
    """
    return np.linalg.norm(arr, axis=1)


def distance_between_points(arr1, arr2):
    """
    Calculate the distance between corresponding points of two NumPy arrays.

    Parameters:
        arr1 (numpy.ndarray): First input array.
        arr2 (numpy.ndarray): Second input array.

    Returns:
        numpy.ndarray: Array containing distances between corresponding points.
    """
    return np.linalg.norm(arr1 - arr2, axis=1)

def threshold_array(arr, threshold):
    """
    Create a new array based on a threshold condition from another array.

    Parameters:
        arr (numpy.ndarray): Input array.
        threshold (float): Threshold value.

    Returns:
        numpy.ndarray: Array with values above threshold set to 1, and 0 otherwise.
    """
    return (arr > threshold).astype(int)

MATS_position_path = "datafiles/MATS_Data/MATS.txt"
MATS_posArray = np.loadtxt(MATS_position_path)
MATS_magnitudes = row_magnitudes(MATS_posArray)
num_datapoints = len(MATS_magnitudes)
#print(num_datapoints)

Positions_folder_path = "datafiles/StarlinkPositions-NumpyArray"
Positions_file_path = get_Positions_filepaths_in_folder(Positions_folder_path)
total_StarlinkSats = len(Positions_file_path)
#print(total_StarlinkSats)

# initialize a numpy array which stores distance between MATS and Starlink Satellies
interSat_distances = np.empty((num_datapoints, total_StarlinkSats))
# initialize a numpy array which stores magnitude of Starlink Satellites from Earth Center
satDistance_magnitudes = np.empty((num_datapoints, total_StarlinkSats))

for i in range(total_StarlinkSats):
    print(f'Processing Starlink Satellite : {i+1} of {total_StarlinkSats}')
    StarlinkSatellite_posArray = np.loadtxt(Positions_file_path[i])
    satDistance_magnitudes[:,i] = row_magnitudes(StarlinkSatellite_posArray)
    interSat_distances[:,i] = distance_between_points(StarlinkSatellite_posArray, MATS_posArray)



earth_radius = Constants.WGS84_EARTH_EQUATORIAL_RADIUS  # in kilometers
visibility_padding_percentage = 1.25
adjusted_radius = (1 + (visibility_padding_percentage/100))*earth_radius

# initialize a numpy array which stores visibility of satellites as a binary values
d = np.empty((num_datapoints, total_StarlinkSats))

# calculating LOS_visibility
for i in range(total_StarlinkSats):
    r1_vals = satDistance_magnitudes[:,i]
    d12_vals = interSat_distances[:,i]
    print(f'Re-processing Starlink Satellite : {i+1} of {total_StarlinkSats}')
    for j in range(num_datapoints):
        d[j,i] = math.sqrt( r1_vals[j]**2 - ( ((d12_vals[j]**2 + r1_vals[j]**2 - MATS_magnitudes[j]**2)**2)/(4 * d12_vals[j]**2) ) )


LOS_visibility = threshold_array(d, adjusted_radius)
np.savetxt(f'datafiles/results/LOS_visibility_data.txt', LOS_visibility, fmt='%d')
