import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_data, is_close_to_target, TARGET_COORDS
import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Relative path
def get_relative_path(*args):
    return os.path.join(current_dir, *args)

# Function to load CSV data
def load_csv_data(file_path, date_column=None):
    try:
        data = pd.read_csv(file_path)
        if date_column:
            data[date_column] = pd.to_datetime(data[date_column])
        st.write(f"Data loaded successfully from {file_path}.")
        return data
    except FileNotFoundError:
        st.error(f"Error: The file {file_path} was not found. Please check the file path.")
    except Exception as e:
        st.error(f"Error loading data from {file_path}: {str(e)}")
    return None

# Load US/ CA Wildfire Data from separate files
modis_data_ca = load_csv_data(get_relative_path('Data', 'NASA wildfires', 'modis_2023_Canada.csv'))
modis_data_us = load_csv_data(get_relative_path('Data', 'NASA wildfires', 'modis_2023_United_States.csv'))
viirs_data_ca = load_csv_data(get_relative_path('Data', 'NASA wildfires', 'viirs-snpp_2023_Canada.csv'))
viirs_data_us = load_csv_data(get_relative_path('Data', 'NASA wildfires', 'viirs-snpp_2023_United_States.csv'))

# Date selection for US/Canada Wildfire Analysis
st.sidebar.header("US/Canada Wildfire Analysis Date")
us_ca_wildfire_date = st.sidebar.date_input(
    "Select Date for US/Canada Wildfire Analysis",
    min_value=pd.to_datetime("2023-01-01").date(),
    max_value=pd.to_datetime("2023-12-31").date(),
    value=pd.to_datetime("2023-06-01").date(),
    key="us_ca_wildfire_date_input"
)

# Filter parameters
min_latitude = 25    # Minimum latitude to properly display USA / CANADA
min_longitude = -130 # Minimum longitude 

# Concatenate and filter Wildfire Data by selected date
if modis_data_ca is not None and modis_data_us is not None and viirs_data_ca is not None and viirs_data_us is not None:
    st.title("Canada and US Wildfire Detections - 2023")

    # Concatenate data for both regions
    modis_data_combined = pd.concat([modis_data_ca, modis_data_us])
    viirs_data_combined = pd.concat([viirs_data_ca, viirs_data_us])

    # Convert the 'acq_date' column to datetime if not already
    modis_data_combined['acq_date'] = pd.to_datetime(modis_data_combined['acq_date'])
    viirs_data_combined['acq_date'] = pd.to_datetime(viirs_data_combined['acq_date'])

    # Filter Wildfire Data by selected date
    modis_filtered_date = modis_data_combined[modis_data_combined['acq_date'].dt.date == us_ca_wildfire_date].copy()
    viirs_filtered_date = viirs_data_combined[viirs_data_combined['acq_date'].dt.date == us_ca_wildfire_date].copy()

    # Filter data without outliers
    modis_filtered = modis_filtered_date[(modis_filtered_date['latitude'] >= min_latitude) & (modis_filtered_date['longitude'] >= min_longitude)]
    viirs_filtered = viirs_filtered_date[(viirs_filtered_date['latitude'] >= min_latitude) & (viirs_filtered_date['longitude'] >= min_longitude)]

    # Plot filtered data without outliers
    st.subheader(f"Fire Detections on {us_ca_wildfire_date}")
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(modis_filtered['longitude'], modis_filtered['latitude'], alpha=0.2, label='MODIS')
    ax.scatter(viirs_filtered['longitude'], viirs_filtered['latitude'], alpha=0.2, label='VIIRS')

    # Overlay target locations
    for coord in TARGET_COORDS:
        ax.plot(coord[1], coord[0], 'r*', markersize=15, label='Target Location' if coord == TARGET_COORDS[0] else "")

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f'Fire Detections in USA and Canada on {us_ca_wildfire_date}')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # Display statistics
    st.write(f"Number of MODIS detections on {us_ca_wildfire_date} after filtering: {len(modis_filtered)}")
    st.write(f"Number of VIIRS detections on {us_ca_wildfire_date} after filtering: {len(viirs_filtered)}")

else:
    st.warning("Wildfire data is not available. Please check the data source.")

# Load Wildfire Data
modis_data, viirs_data = load_data(
    get_relative_path('Data', 'NASA wildfires', 'modis_combined.csv'),
    get_relative_path('Data', 'NASA wildfires', 'viirs_combined.csv')
)

# Date selection for Wildfire Analysis
st.sidebar.header("Wildfire Analysis Date")
june_day = st.sidebar.slider(
    "Select day in June 2023",
    min_value=1,
    max_value=30,
    value=1,
    step=1,
    key="june_day_slider"
)
analysis_date = pd.to_datetime(f"2023-06-{june_day:02d}").date()

# Wildfire Analysis Section
if modis_data is not None and viirs_data is not None:
    st.title("Canada Wildfire Detections - June 2023")
    # Filter Wildfire Data by selected date
    modis_filtered = modis_data[modis_data['acq_date'].dt.date == analysis_date].copy()
    viirs_filtered = viirs_data[viirs_data['acq_date'].dt.date == analysis_date].copy()

    # Display Wildfire Data
    if len(modis_filtered) == 0 and len(viirs_filtered) == 0:
        st.info(f"No wildfire data recorded for these locations on {analysis_date}.")
    else:
        # Proximity filter
        modis_filtered['is_close'] = modis_filtered.apply(lambda row: is_close_to_target(row['latitude'], row['longitude']), axis=1)
        viirs_filtered['is_close'] = viirs_filtered.apply(lambda row: is_close_to_target(row['latitude'], row['longitude']), axis=1)

        modis_filtered = modis_filtered[modis_filtered['is_close']]
        viirs_filtered = viirs_filtered[viirs_filtered['is_close']]

        # Plotting Wildfire Detections
        st.subheader(f"Wildfire Detections on {analysis_date}")
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(modis_filtered['longitude'], modis_filtered['latitude'], alpha=0.5, label='MODIS')
        ax.scatter(viirs_filtered['longitude'], viirs_filtered['latitude'], alpha=0.5, label='VIIRS')

        # Plot target locations
        for coord in TARGET_COORDS:
            ax.plot(coord[1], coord[0], 'r*', markersize=13)

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title(f'Fire Detections near Target Coordinates ({analysis_date})')
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # Display statistics
        st.write(f"Number of MODIS detections: {len(modis_filtered)}")
        st.write(f"Number of VIIRS detections: {len(viirs_filtered)}")

# Air Quality Analysis Section
st.title("Air Quality Analysis")

# Load refined data for all pollutants
base_path = get_relative_path('Data', 'EPA')
pm25_data = pd.read_csv(os.path.join(base_path, '2.5', 'combined_2.5_data.csv'))
co_data = pd.read_csv(os.path.join(base_path, 'CO', 'combined_co_data.csv'))
no2_data = pd.read_csv(os.path.join(base_path, 'NO2', 'combined_no2_data.csv'))
ozone_data = pd.read_csv(os.path.join(base_path, 'Ozone', 'combined_ozone_data.csv'))

# Convert Date columns to datetime format
for df in [pm25_data, co_data, no2_data, ozone_data]:
    df['Date'] = pd.to_datetime(df['Date'])

# Create pollutant_data dictionary with correct column names
pollutant_data = {
    'PM2.5': (pm25_data, 'Daily Mean PM2.5 Concentration'),
    'CO': (co_data, 'Daily Max 8-hour CO Concentration'),
    'NO2': (no2_data, 'Daily Max 1-hour NO2 Concentration'),
    'Ozone': (ozone_data, 'Daily Max 8-hour Ozone Concentration')
}

# Define target counties
target_counties = ['New York', 'Philadelphia', 'District of Columbia', 'Suffolk']

# Define date range (3 days before and after the selected date)
date_range = pd.date_range(start=analysis_date - pd.Timedelta(days=3), 
                           end=analysis_date + pd.Timedelta(days=3))

# Filter data for the date range and target counties
filtered_data = {
    pollutant: df[
        (df['Date'].dt.date.isin(date_range.date)) & 
        (df['County'].isin(target_counties))
    ] for pollutant, (df, _) in pollutant_data.items()
}

# Create a 2x2 subplot
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

# Plot for each pollutant
for i, (pollutant, data) in enumerate(filtered_data.items()):
    conc_column = pollutant_data[pollutant][1]
    sns.lineplot(data=data, x='Date', y=conc_column, hue='County', marker='o', ax=axs[i])
    axs[i].set_title(f'{pollutant} Levels')
    axs[i].set_xlabel('Date')
    axs[i].set_ylabel('Concentration')
    axs[i].tick_params(axis='x', rotation=45)
    axs[i].axvline(analysis_date, color='r', linestyle='--', label='Selected Date')
    axs[i].legend(title='County', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
st.pyplot(fig)

# Display summary statistics
st.subheader("Summary Statistics")
selected_pollutant = st.selectbox("Select a pollutant to view summary statistics", list(pollutant_data.keys()))
conc_column = pollutant_data[selected_pollutant][1]
summary_stats = filtered_data[selected_pollutant].groupby('County')[conc_column].describe()
st.write(summary_stats)

# Display raw data
st.subheader("Raw Air Quality Data")
selected_pollutant_raw = st.selectbox("Select a pollutant to view raw data", list(pollutant_data.keys()))
st.write(filtered_data[selected_pollutant_raw])

# Air Quality Correlation Analysis Section
st.title("Air Quality Correlation Analysis")

# Date selection for Air Quality Correlation Analysis
st.sidebar.header("Air Quality Correlation Date")
june_day = st.sidebar.slider(
    "Select day in June 2023 for correlation analysis",
    min_value=1,
    max_value=30,
    value=1,
    step=1,
    key="june_day_correlation_slider"
)
correlation_date = pd.to_datetime(f"2023-06-{june_day:02d}").date()

# Dictionary to map pollutant names to their file paths and concentration column names
pollutant_info = {
    'Ozone': ('Ozone/combined_ozone_data.csv', 'Daily Max 8-hour Ozone Concentration'),
    'CO': ('CO/combined_co_data.csv', 'Daily Max 8-hour CO Concentration'),
    'NO2': ('NO2/combined_no2_data.csv', 'Daily Max 1-hour NO2 Concentration'),
    'PM2.5': ('2.5/combined_2.5_data.csv', 'Daily Mean PM2.5 Concentration')
}

# Function to load and preprocess all pollutant data
@st.cache_data
def load_all_pollutant_data():
    all_data = {}
    for pollutant, (file_name, column_name) in pollutant_info.items():
        df = pd.read_csv(get_relative_path('Data', 'EPA', file_name))
        df['Date'] = pd.to_datetime(df['Date'])
        df = df[df['Date'].dt.month == 6]  # Filter for June
        df = df[['Date', 'County', column_name]]
        df = df.rename(columns={column_name: pollutant})
        all_data[pollutant] = df
    return all_data

# Load all pollutant data
all_pollutant_data = load_all_pollutant_data()

# Merge datasets
merged_data = all_pollutant_data['Ozone']
for pollutant in ['CO', 'NO2', 'PM2.5']:
    merged_data = merged_data.merge(all_pollutant_data[pollutant], on=['Date', 'County'], how='outer')

# Filter data for the selected date
filtered_data = merged_data[merged_data['Date'].dt.date == correlation_date]

if not filtered_data.empty:
    # Calculate correlations
    correlation_matrix = filtered_data[list(pollutant_info.keys())].corr()

    # Visualize correlations
    st.subheader(f"Correlation of Pollutant Levels on {correlation_date}")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)