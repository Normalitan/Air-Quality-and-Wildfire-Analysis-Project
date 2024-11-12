# TheFinal
# Air Quality and Wildfire Analysis Project

Download Data: https://drive.google.com/file/d/1Gz5400th6gRVkiTyDT3lro6Er8VE6-Uy/view?usp=sharing

## Overview
This project continues to analyze the relationship between wildfires and air quality in the Northeastern United States in 4 counties (Norfol, Sulfolk, Philly, and District of Columbiaa), with a focus on the impact of Canadian wildfires around June 7th 2023. The project utilizes data from NASA's FIRMS (Fire Information for Resource Management System) and the EPA (Environmental Protection Agency) to explore correlations between wildfire occurrences and air quality measurements.

## Files
1. EPA API.ipynb: Jupyter notebook for fetching and processing EPA air quality data. (INCOMPLETE)
2. FIRMS API NASA.ipynb: Jupyter notebook for fetching and processing NASA FIRMS wildfire data. (INCOMPLETE)
3. NASA FIRMS EDA.ipynb: Exploratory Data Analysis of the NASA FIRMS wildfire data.
4. EPA EDA.ipynb: Exploratory Data Analysis of the EPA air quality data.
5. SteamLit.py: Streamlit application for interactive visualization and analysis of the data.

## Objectives
- Integrate data from multiple APIs to compare consistency across data sources.
- Analyze air quality trends in the US Northeast Coast, focusing on the impact of June 7th Canadian wildfire.

## Key Features
Data collection from EPA and NASA FIRMS APIs
Data preprocessing and cleaning
Exploratory Data Analysis (EDA) of both wildfire and air quality data
Visualization of wildfire detections and air quality measurements
Correlation analysis between different air pollutants
Interactive Streamlit application for data exploration and visualization

## Streamlit Application
The Streamlit app (SteamLit.py) provides an interactive interface for:
1. Visualizing wildfire detections across the US and Canada
2. Analyzing air quality data for specific pollutants (PM2.5, CO, NO2, Ozone)
3. Exploring correlations between different air pollutants
4. Viewing summary statistics and raw data for air quality measurements

# Data Sources
EPA Air Quality Data
NASA FIRMS Wildfire Data (MODIS and VIIRS satellite data)

Technologies Used
Python
Pandas for data manipulation
Matplotlib and Seaborn for data visualization
Streamlit for creating the interactive web application

This project combines extensive data analysis with interactive visualization to provide insights into the relationship between wildfires and air quality, focusing on recent events affecting the Northeastern United States.
