Codework for Orbit Propagation and Analysis using TLEs

# Enviroment Setup
A virtual environment has bees used on the local machine (running Debian 12 bookworm) to establish the working. The requirements to setup the virtual enviroment can be installed using 'pip' and the 'requirements.txt' file.

The requirements.txt file has been obtained using
```bash
pip freeze > requirements.txt
```

These can be used to set-up the necessary virtual environment using
```bash
pip install -r requirements.txt
```

# Objective of the Project
## Propagate MATS Satellite in Orbit using TLEs
The MATS Satellite is propagated in time using the TLEs. The evolution of the satellite orbit over time is examined.

The elevation of the satellite as seen from teh Esrange Ground Station has also been plotted.

## Find the number of Starlink Satellites in Line-of-Site of MATS
For a fixed time-period, all the Starlink satellites and the MATS satellite is propagated and the number of satellites in Line-of-site of MATS are examined. The StarlinkData-2023 folder stores the data of a few starlink satellites for the year 2023. The files names in the folder correspond to the NORAD Catalog ID of the satellites.

The available data for some satellites is only upto the first 35 days of 2023. This, along with the number of satellites taken into consideration (439 satellites) is the reason for the analysis being limited to January 2023.

### Mathematical Formulation
The analysis has been simplified by assuming the Earth to be a sphere of constant radius equal to the WGS84_EARTH_EQUATORIAL_RADIUS.
