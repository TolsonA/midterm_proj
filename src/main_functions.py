import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.all_data = None

    def read_data(self):
        """Reads the cyclone data from a file and initializes the all_data attribute."""
        cyclone_data = []
        current_cyclone = None
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.startswith('AL'): #Goes through each line to find AL, which means new cyclone.
                    if current_cyclone is not None:
                        cyclone_data.append(current_cyclone)
                    current_cyclone = {'header': line.strip(), 'data': []} #AL header/dict
                else:
                    if current_cyclone is not None:
                        current_cyclone['data'].append(line.strip().split(','))
        if current_cyclone is not None:
            cyclone_data.append(current_cyclone)

        all_cyclone_dfs = []
        """I need to turn this into a dataframe and then add in columns. Columns are based on NHC data ref sheet"""
        for cyclone in cyclone_data:
            df = pd.DataFrame(cyclone['data'], columns=['Date', 'Time', 'Record', 'Status', 'Latitude', 'Longitude', 'WindSpeed', 'Pressure',
                                                        'Rad_34_NE', 'Rad_34_SE', 'Rad_34_SW', 'Rad_34_NW', 'Rad_50_NE', 'Rad_50_SE',
                                                        'Rad_50_SW', 'Rad_50_NW', 'Rad_64_NE', 'Rad_64_SE', 'Rad_64_SW', 'Rad_64_NW', 'Rad_maxwnd'])
            # Define each column type. Creates Datetime & Cyclone column.                        
            df['Date'] = df['Date'].astype(str)
            df['Time'] = df['Time'].astype(str)
            df['Latitude'] = df['Latitude'].apply(self.convert_lat_lon)
            df['Longitude'] = df['Longitude'].apply(self.convert_lat_lon)
            df['WindSpeed'] = df['WindSpeed'].astype(int)
            df['Pressure'] = df['Pressure'].astype(int)
            df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y%m%d %H%M')
            df.set_index('Datetime', inplace=True)
            df['Cyclone'] = cyclone['header']
            all_cyclone_dfs.append(df)
        self.all_data = pd.concat(all_cyclone_dfs)

    # No value input needed for static method. Used above for data provided. 
    @staticmethod
    def convert_lat_lon(value):
        """Converts latitude and longitude to float values."""
        if 'N' in value or 'E' in value:
            return float(value[:-1])
        elif 'S' in value or 'W' in value:
            return -float(value[:-1])
    
"""Below: applies latitude and longitude filters and initializes the filtered_data attribute."""
class DataFilter:
    def __init__(self, all_data):
        self.all_data = all_data
        self.filtered_data = None

    def filter_data(self, min_lat, max_lat, min_lon, max_lon):
        self.filtered_data = self.all_data[(self.all_data['Latitude'] >= min_lat) & (self.all_data['Latitude'] <= max_lat) &
                                           (self.all_data['Longitude'] >= min_lon) & (self.all_data['Longitude'] <= max_lon)]
        self.filtered_data['Year'] = self.filtered_data.index.year

class CycloneCalculator:
    def __init__(self, filtered_data):
        self.filtered_data = filtered_data
        self.cyclones_per_year = None

    def calculate_cyclones_per_year(self):
        """Groups data by year and counts unique cyclones, initializes the cyclones_per_year attribute."""
        self.cyclones_per_year = self.filtered_data.groupby('Year')['Cyclone'].nunique()
        all_years = pd.Series(0, index=np.arange(self.filtered_data['Year'].min(), self.filtered_data['Year'].max() + 1))
        self.cyclones_per_year = self.cyclones_per_year.reindex(all_years.index, fill_value=0)

class FilteredTrendlinePlot:
    def __init__(self, cyclones_per_year):
        self.cyclones_per_year = cyclones_per_year
        self.trendline_values = None
        self.extended_years = None

    def calculate_trendline(self):
        """Calculates the trend line for the data and initializes the trendline_values and extended_years attributes."""
        z = np.polyfit(self.cyclones_per_year.index, self.cyclones_per_year.values, 2)
        p = np.poly1d(z)
        last_year = self.cyclones_per_year.index.max()
        future_years = np.arange(last_year + 1, last_year + 27)
        self.extended_years = np.concatenate((self.cyclones_per_year.index, future_years))
        self.trendline_values = p(self.extended_years)
        

    def plot_cyclone_data(self):
        smoothed_data = self.cyclones_per_year.rolling(window=5).mean()
        """Plots the cyclone data with trend lines and data labels, uses rolling mean."""
        plt.figure(figsize=(12, 6)) 
        plt.plot(smoothed_data.index, smoothed_data.values, label='Smoothed Number of Cyclones')
        #plt.bar(self.cyclones_per_year.index, self.cyclones_per_year.values, label='Number of Cyclones')
        plt.plot(self.extended_years, self.trendline_values, "r--", label='Trend Line')

        #for index, value in enumerate(self.cyclones_per_year.values):
        #    plt.text(self.cyclones_per_year.index[index], value, str(value), ha='center', va='bottom')

        plt.title('Total Number of Cyclones per Year with Forecast (Filtered by Lat/Lon)')
        plt.xlabel('Year')
        plt.ylabel('Number of Cyclones')
        plt.ylim(bottom=0)
        plt.legend()
        plt.grid(True)
        plt.show()

class NoFilterTrendlinePlot:
    def __init__(self, all_data):
        self.all_data = all_data
        self.cyclones_per_year = None
        self.trendline_values = None
        self.extended_years = None

    def calculate_cyclones_per_year(self):
        """Groups data by year and counts unique cyclones, initializes the cyclones_per_year attribute."""
        self.all_data['Year'] = self.all_data.index.year
        self.cyclones_per_year = self.all_data.groupby('Year')['Cyclone'].nunique()
        all_years = pd.Series(0, index=np.arange(self.all_data['Year'].min(), self.all_data['Year'].max() + 1))
        self.cyclones_per_year = self.cyclones_per_year.reindex(all_years.index, fill_value=0)

    def calculate_trendline(self):
        """Calculates the trend line for the data and initializes the trendline_values and extended_years attributes."""
        z = np.polyfit(self.cyclones_per_year.index, self.cyclones_per_year.values, 2)
        p = np.poly1d(z)
        last_year = self.cyclones_per_year.index.max()
        future_years = np.arange(last_year + 1, last_year + 27)
        self.extended_years = np.concatenate((self.cyclones_per_year.index, future_years))
        self.trendline_values = p(self.extended_years)

    def plot_cyclone_data(self):
        """Plots the cyclone data with trend lines and data labels."""
        plt.figure(figsize=(12, 6))
        plt.plot(self.cyclones_per_year.index, self.cyclones_per_year.values, marker='o', label='Number of Cyclones')
        plt.plot(self.extended_years, self.trendline_values, "r--", label='Trend Line')

        #for index, value in enumerate(self.cyclones_per_year.values):
        #    plt.text(self.cyclones_per_year.index[index], value, str(value), ha='center', va='bottom')

        plt.title('Total Number of Cyclones per Year with Forecast')
        plt.xlabel('Year')
        plt.ylabel('Number of Cyclones')
        plt.ylim(bottom=0)
        plt.legend()
        plt.grid(True)

def main():
    file_path = '../data/hurdat2_1851_2023.txt'
    min_lat = 27.5
    max_lat = 29.4
    min_lon = -81.5
    max_lon = -78.8

    # Reading and converting data
    reader = DataReader(file_path)
    reader.read_data()
    
    # Filtering data
    filterer = DataFilter(reader.all_data)
    filterer.filter_data(min_lat, max_lat, min_lon, max_lon)
    
    # Calculating cyclones per year
    calculator_filtered = CycloneCalculator(filterer.filtered_data)
    calculator_filtered.calculate_cyclones_per_year()
    
    # Calculating trendline and plotting data for filtered data
    plotter_filtered = FilteredTrendlinePlot(calculator_filtered.cyclones_per_year)
    plotter_filtered.calculate_trendline()
    plotter_filtered.plot_cyclone_data()

    # Calculating cyclones per year and plotting for unfiltered data
    plotter_unfiltered = NoFilterTrendlinePlot(reader.all_data)
    plotter_unfiltered.calculate_cyclones_per_year()
    plotter_unfiltered.calculate_trendline()
    plotter_unfiltered.plot_cyclone_data()

# Run the main function
#main()
