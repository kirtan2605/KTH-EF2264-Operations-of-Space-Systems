import os
import numpy as np
import matplotlib.pyplot as plt

def plot_array_as_grid(arr):
    """
    Plot a NumPy array as a grid with green for 1 and red for 0.

    Parameters:
        arr (numpy.ndarray): Input array.

    Returns:
        None
    """

    # Determine the maximum dimension of the array
    max_dim = max(arr.shape)

    # Set the figure size to be square and proportional to the maximum dimension
    size = (max_dim, max_dim)

    plt.figure(figsize=size)  # Adjust figure size as needed

    # Plot the array as a grid
    plt.imshow(arr, cmap='RdYlGn', interpolation='nearest')

    # Add color bar legend
    plt.colorbar(label='Value')

    plt.show()


LOS_results_path = "datafiles/LOS_visibility_data.txt"
LOS_results = np.loadtxt(LOS_results_path)

plot_array_as_grid(LOS_results)
