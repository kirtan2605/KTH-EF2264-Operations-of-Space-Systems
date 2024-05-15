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

MATS_position_path = "MATS.txt"
MATS_posArray = np.loadtxt(MATS_position_path)
MATS_magnitudes = row_magnitudes(MATS_posArray)
num_datapoints = len(MATS_magnitudes)

Starlink_position_path = "Starlink_002.txt"
Starlink_posArray = np.loadtxt(Starlink_position_path)
Starlink_magnitudes = row_magnitudes(Starlink_posArray)

interSat_distances = distance_between_points(Starlink_posArray, MATS_posArray)

np.savetxt(f'interSat_distances_data.txt', interSat_distances)

earth_radius = Constants.WGS84_EARTH_EQUATORIAL_RADIUS  # in meters
visibility_padding_percentage = 1.25
adjusted_radius = (1 + (visibility_padding_percentage/100))*earth_radius

# initialize a numpy array which stores visibility of satellites as a binary values
d = np.empty(num_datapoints)

# calculating LOS_visibility
for j in range(num_datapoints):
    d[j] = math.sqrt( Starlink_magnitudes[j]**2 - ( ((interSat_distances[j]**2 + Starlink_magnitudes[j]**2 - MATS_magnitudes[j]**2)**2)/(4 * interSat_distances[j]**2) ) )


LOS_visibility = threshold_array(d, adjusted_radius)
np.savetxt(f'LOS_visibility_data.txt', LOS_visibility, fmt='%d')
