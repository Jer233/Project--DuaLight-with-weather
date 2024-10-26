import pandas as pd
import random
import xml.etree.ElementTree as ET

# Load your weather data
weather_data = pd.read_csv('weather_data_finglin.csv')

# Convert the 'DATE' column to datetime if it's not already in datetime format
weather_data['DATE'] = pd.to_datetime(weather_data['DATE'])

# Define the date range
start_date = pd.to_datetime('2024-05-28')
end_date = pd.to_datetime('2024-08-21')

# Filter the weather data to only include the range between 2024/5/28 and 2024/8/21
filtered_weather_date = weather_data[(weather_data['DATE'] >= start_date) & (weather_data['DATE'] <= end_date)]

# Ensure there's data in the filtered range
if filtered_weather_date.empty:
    raise ValueError("No weather data available for the specified date range.")

# Randomly select one day's weather from the filtered dataset (for the whole simulation)
selected_date = filtered_weather_date.sample(1).iloc[0]

# Extract the selected day's weather conditions
tmax = selected_date['TMAX']
prcp = selected_date['PRCP']
selected_day = selected_date['DATE']

# Print the selected day
print(f"Selected weather data from: {selected_day}")

# Parse the route file
route_file = 'cologne8.rou.xml'

# Define thresholds for weather conditions
temp_threshold = 303.15  # Speed will increase if TMAX > 30
prcp_threshold = 80  # Speed will decrease if PRCP > 10

tree = ET.parse(route_file)
root = tree.getroot()


# Loop through each trip in the route file
for trip in root.findall('trip'):
    # Default speed factor (no change)
    speed_factor = 1.0
    
    # Adjust speed based on temperature
    if tmax > temp_threshold:
        speed_factor += random.uniform(0, 0.2) # Randomly increase speed within 0 to 0.2
    
    # Adjust speed based on precipitation
    if prcp > prcp_threshold:
        speed_factor -= random.uniform(0, 0.2) # Randomly decrease speed within 0 to 0.2
    
    # Ensure the speed factor remains positive
    speed_factor = max(speed_factor, 0.1)
    
    # Modify the `departSpeed` and `speedFactor` attributes
    trip.set('departSpeed', 'max')  # Set to max initially
    trip.set('speedFactor', str(speed_factor))  # Adjust the speed factor

# Save the modified route file
modified_file = 'cologne8_modified_rainy.rou.xml'
tree.write(modified_file)

print("cologne8 updated with weather-based speed adjustments.")

