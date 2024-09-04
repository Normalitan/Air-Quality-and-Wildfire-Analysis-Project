# utils.py
import pandas as pd
from geopy.distance import geodesic

# Target coordinates
TARGET_COORDS = [
    (48.8101, -76.3605),
    (53.08228, -75.44976),
    (52.7008, -73.5289),
    (50.470, -74.259)
]

# Function to check if a point is close to any target coordinate
def is_close_to_target(lat, lon, max_distance_km=50):
    try:
        return any(geodesic((lat, lon), target).km <= max_distance_km for target in TARGET_COORDS)
    except:
        return False

# load data
def load_data(modis_file, viirs_file):
    try:
        modis_data = pd.read_csv(modis_file)
        viirs_data = pd.read_csv(viirs_file)

        # Convert acquisition date to datetime
        modis_data['acq_date'] = pd.to_datetime(modis_data['acq_date'])
        viirs_data['acq_date'] = pd.to_datetime(viirs_data['acq_date'])

        return modis_data, viirs_data
    except Exception as e:
        raise Exception(f"Error loading data: {e}")
