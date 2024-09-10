import csv
from datetime import datetime, timedelta
import random
import pytz

# Configurations
time_zone = pytz.timezone('Asia/Ho_Chi_Minh')
end_date = datetime.now(time_zone)

start_date = end_date - timedelta(days=4)
time_interval = timedelta(minutes=5)
api_key = 'TEY8OO5iafAV96gRKcZohbO6ED'

# Sensor configurations with their respective value ranges
sensors = [
    {'pin': 'V8', 'name': 'sensor_temp', 'base_range': (22.0, 24.0)},
    {'pin': 'V7', 'name': 'sensor_hum', 'base_range': (55.0, 65.0)},
    {'pin': 'V9', 'name': 'sensor_temp_water', 'base_range': (19.0, 22.0)},
    {'pin': 'V5', 'name': 'sensor_ph', 'base_range': (5.5, 6.5)},
    {'pin': 'V4', 'name': 'sensor_light', 'base_range': (0.0, 100.0)}
]

# Helper function to adjust range based on time
def adjust_range(sensor, current_time):
    hour = current_time.hour
    if sensor['name'] == 'sensor_temp':
        if 6 <= hour < 18:  # Daytime
            return (sensor['base_range'][0] + 5, sensor['base_range'][1] + 5)
        else:  # Nighttime
            return sensor['base_range']
    elif sensor['name'] == 'sensor_hum':
        if 6 <= hour < 18:  # Daytime
            return sensor['base_range']
        else:  # Nighttime
            return (sensor['base_range'][0] + 10, sensor['base_range'][1] + 10)
    elif sensor['name'] == 'sensor_light':
        if 6 <= hour < 18:  # Daytime
            return (70.0, 90.0)
        else:  # Nighttime
            return (0.0, 10.0)
    return sensor['base_range']

# Generate data
data = []
current_time = end_date
while current_time >= start_date:
    for sensor in sensors:
        adjusted_range = adjust_range(sensor, current_time)
        value = round(random.uniform(*adjusted_range), 1)
        data.append([api_key, sensor['pin'], sensor['name'], value, current_time.strftime('%Y-%m-%d %H:%M:%S')])
    current_time -= time_interval

# Write to CSV
with open('sensors_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['api_key', 'pin', 'name', 'value', 'date'])
    csvwriter.writerows(data)


