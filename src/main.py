import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_path = 'data/hurdat2_1851_2023.txt'

data_chunks = []

column_names = ['Date', 'Time', 'Record ID', 'Status', 
                'Latitude', 'Longitude', 'WindSpeed', 
                'Pressure', 'Rad_34_NE', 'Rad_34_SE', 
                'Rad_34_SW', 'Rad_34_NW', 'Rad_50_NE', 'Rad_50_SE',
                'Rad_50_SW', 'Rad_50_NW', 'Rad_64_NE', 'Rad_64_SE', 
                'Rad_64_SW', 'Rad_64_NW', 'Rad_maxwnd']

def convert_lat_lon(value):
    if 'N' in value or 'E' in value:
        return float(value[:-1])
    elif 'S' in value or 'W' in value:
        return -float(value[:-1])
    
with open(file_path, 'r') as file:
    for line in file:
        # Check if the line starts with 'AL' and has a header format
        if line.startswith('AL'):
            continue
        # Split the line into columns and append to the data_chunks list
        data_chunks.append(line.strip().split(','))

data = pd.DataFrame(data_chunks, columns=column_names)

data['Date'] = data['Date'].astype(str)
data['Time'] = data['Time'].astype(str)
data['Latitude'] = data['Latitude'].apply(convert_lat_lon)
data['Longitude'] = data['Longitude'].apply(convert_lat_lon)
data['WindSpeed'] = data['WindSpeed'].astype(int)
data['Pressure'] = data['Pressure'].astype(int)
data['Rad_maxwnd'] = data['Rad_maxwnd'].astype(int)

data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%Y%m%d %H%M')
data.set_index('Datetime', inplace=True)

# min/max lat/lon to get storms that impacted the specified area. 
min_lat, max_lat = 27.5, 29.4
min_lon, max_lon = -81.5, -78.8

# The following filter provides 271 rows of data all affecting the Space Coast.
filtered_data = data[(data['Latitude'] >= min_lat) & 
                     (data['Latitude'] <= max_lat) &
                     (data['Longitude'] >= min_lon) & 
                     (data['Longitude'] <= max_lon)]

print(filtered_data.head())