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
pin = 'V1'
name = 'Nhiệt độ'
temperature_range = (25.0, 27.0)

# Generate data
data = []
current_time = end_date
while current_time >= start_date:
    value = round(random.uniform(*temperature_range), 1)
    data.append([api_key, pin, name, value, current_time.strftime('%Y-%m-%d %H:%M:%S')])
    current_time -= time_interval

# Write to CSV
with open('1_tem.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['api_key', 'pin', 'name', 'value', 'date'])
    csvwriter.writerows(data)

print(f"Generated {len(data)} rows of data")
