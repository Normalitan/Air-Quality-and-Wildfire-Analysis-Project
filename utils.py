import pandas as pd
from geopy.distance import geodesic
import gdown
import os
import zipfile

# Download and extract ZIP from Google Drive if folder doesn't exist
def download_and_extract_if_needed(local_zip, extract_to, file_id):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to, exist_ok=True)
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, local_zip, quiet=False)
        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

# Target coordinates (for proximity filtering)
TARGET_COORDS = [
    (48.8101, -76.3605),
    (53.08228, -75.44976),
    (52.7008, -73.5289),
    (50.470, -74.259)
]

# Check if a point is close to any target coordinate
def is_close_to_target(lat, lon, max_distance_km=50):
    try:
        return any(geodesic((lat, lon), target).km <= max_distance_km for target in TARGET_COORDS)
    except:
        return False

# Load MODIS and VIIRS data with date parsing
def load_data(modis_file, viirs_file):
    try:
        modis_data = pd.read_csv(modis_file)
        viirs_data = pd.read_csv(viirs_file)

        modis_data['acq_date'] = pd.to_datetime(modis_data['acq_date'])
        viirs_data['acq_date'] = pd.to_datetime(viirs_data['acq_date'])

        return modis_data, viirs_data
    except Exception as e:
        raise Exception(f"Error loading data: {e}")
