import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# List of functions

# file path to data
file_path = 'data/hurdat2_1851_2023.txt'

# Reading the file
def read_data(file_path):
    """Reads the text data from file and returns a list of cyclone data."""
    cyclone_data = []
    current_cyclone = None
    """Taking the headers out that. Always starts with AL if using Atlantic Basin"""
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('AL'):
                if current_cyclone is not None:
                    cyclone_data.append(current_cyclone)
                current_cyclone = {'header': line.strip(), 'data': []}
            else:
                if current_cyclone is not None:
                    current_cyclone['data'].append(line.strip().split(','))
    if current_cyclone is not None:
        cyclone_data.append(current_cyclone)
    return cyclone_data

# Cleans
def process_cyclone_data(cyclone_data):
    """Processes the cyclone data and returns a concatenated DataFrame."""
    all_cyclone_dfs = []
    for cyclone in cyclone_data:
        df = pd.DataFrame(cyclone['data'], columns=['Date', 'Time', 'Record', 'Status', 'Latitude', 'Longitude', 'WindSpeed', 'Pressure',
                                                    'Rad_34_NE', 'Rad_34_SE', 'Rad_34_SW', 'Rad_34_NW', 'Rad_50_NE', 'Rad_50_SE',
                                                    'Rad_50_SW', 'Rad_50_NW', 'Rad_64_NE', 'Rad_64_SE', 'Rad_64_SW', 'Rad_64_NW'])
        # Convert data types where necessary
        df['Date'] = df['Date'].astype(str)
        df['Time'] = df['Time'].astype(str)
        df['Latitude'] = df['Latitude'].apply(convert_lat_lon)
        df['Longitude'] = df['Longitude'].apply(convert_lat_lon)
        df['WindSpeed'] = df['WindSpeed'].astype(int)
        df['Pressure'] = df['Pressure'].astype(int)
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y%m%d %H%M')
        df.set_index('Datetime', inplace=True)
        df['Cyclone'] = cyclone['header']
        all_cyclone_dfs.append(df)
    all_data = pd.concat(all_cyclone_dfs)
    return all_data


# This function removes the N or E for latitude and S or W for longitude. Allows lat/lon to be float.
def convert_lat_lon(value):
    if 'N' in value or 'E' in value:
        return float(value[:-1])
    elif 'S' in value or 'W' in value:
        return -float(value[:-1])
    
def filter_data(all_data, min_lat, max_lat, min_lon, max_lon):
    """Applies latitude and longitude filters and returns the filtered data."""
    filtered_data = all_data[(all_data['Latitude'] >= min_lat) & (all_data['Latitude'] <= max_lat) &
                            (all_data['Longitude'] >= min_lon) & (all_data['Longitude'] <= max_lon)]
    return filtered_data

def plot_cyclone_data(cyclones_per_year, trendline_values, extended_years):
    """Plots the cyclone data with trend lines and data labels."""
    plt.figure(figsize=(10, 6))
    plt.bar(cyclones_per_year.index, cyclones_per_year.values, label='Number of Cyclones')
    plt.plot(extended_years, trendline_values, "r--", label='Trend Line')

    # Add data labels
    for index, value in enumerate(cyclones_per_year.values):
        plt.text(cyclones_per_year.index[index], value, str(value), ha='center', va='bottom')

    plt.title('Total Number of Cyclones per Year with Forecast (Filtered by Lat/Lon)')
    plt.xlabel('Year')
    plt.ylabel('Number of Cyclones')
    plt.ylim(bottom=0)
    plt.legend()
    plt.grid(True)
    plt.show()


def main(file_path, min_lat, max_lat, min_lon, max_lon):
    cyclone_data = read_data(file_path)
    all_data = process_cyclone_data(cyclone_data)
    
    # Move the Cyclone column to the first position
    columns = ['Cyclone'] + [col for col in all_data.columns if col != 'Cyclone']
    all_data = all_data[columns]

    filtered_data = filter_data(all_data, min_lat, max_lat, min_lon, max_lon)

    # Extract the year from the Datetime column
    filtered_data['Year'] = filtered_data.index.year

    # Group by year and count unique cyclones
    cyclones_per_year = filtered_data.groupby('Year')['Cyclone'].nunique()

    # Create a complete range of years
    all_years = pd.Series(0, index=np.arange(filtered_data['Year'].min(), filtered_data['Year'].max() + 1))

    # Reindex the cyclones_per_year series to include all years
    cyclones_per_year = cyclones_per_year.reindex(all_years.index, fill_value=0)

    # Calculate the trend line
    z = np.polyfit(cyclones_per_year.index, cyclones_per_year.values, 1)
    p = np.poly1d(z)

    # Define the future range for forecasting
    last_year = cyclones_per_year.index.max()
    future_years = np.arange(last_year + 1, last_year + 11)

    # Combine the historical and future years
    extended_years = np.concatenate((cyclones_per_year.index, future_years))

    # Calculate the trendline values for the extended range
    trendline_values = p(extended_years)

    plot_cyclone_data(cyclones_per_year, trendline_values, extended_years)


# Parameters
file_path = 'data/hurdat2_1851_2023.txt'
min_lat = 27.5
max_lat = 29.4
min_lon = -81.5
max_lon = -78.8


# Run the main function
#main(file_path, min_lat, max_lat, min_lon, max_lon)