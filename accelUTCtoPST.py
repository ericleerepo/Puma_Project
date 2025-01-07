#converts time in accelerometer csv from UTC to PST

import os
import pandas as pd
from datetime import datetime, timedelta

# Define the base folder
base_folder = '123F_accel copy'

# Define the time difference from UTC to PST
time_difference = timedelta(hours=-8)

# Collect all files into a single list before reorganization
all_files = []
for day_folder in sorted(os.listdir(base_folder)):
    day_path = os.path.join(base_folder, day_folder)
    if os.path.isdir(day_path) and day_folder.isdigit():
        for hour_file in os.listdir(day_path):
            if hour_file.endswith('.csv'):
                hour_path = os.path.join(day_path, hour_file)
                all_files.append((day_folder, hour_file, hour_path))

# Reorganize files into the base folder and adjust time
for day_folder, hour_file, hour_path in all_files:
    # Load the CSV file into a DataFrame
    df = pd.read_csv(hour_path)

    # Convert the 'time' column from UTC to PST
    if 'FullDatetime' in df.columns:
        df['FullDatetime'] = pd.to_datetime(df['FullDatetime']) + time_difference
        df['FullDatetime'] = df['FullDatetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    if 'UTC DateTime' in df.columns:
        df['UTC DateTime'] = pd.to_datetime(df['UTC DateTime'], format='%H:%M:%S') + time_difference
        df['UTC DateTime'] = df['UTC DateTime'].dt.strftime('%H:%M:%S')

    # Calculate new hour and adjust for day change
    original_datetime = datetime.strptime(hour_file.split('.')[0], '%Y-%m-%d-%H')
    new_datetime = original_datetime + time_difference

    print(f"{original_datetime.strftime('%Y-%m-%d-%H')} moved to {new_datetime.strftime('%Y-%m-%d-%H')}")

    new_day_folder = new_datetime.strftime('%y%m%d')
    new_day_path = os.path.join(base_folder, new_day_folder)
    if not os.path.exists(new_day_path):
        os.makedirs(new_day_path)

    # Move the file to the base folder with the new name
    new_hour_file = f"{new_datetime.strftime('%Y-%m-%d-%H')}.csv"
    new_hour_path = os.path.join(new_day_path, new_hour_file)
    os.rename(hour_path, new_hour_path)

    print(f"{hour_file} moved to {new_hour_file}")

# Remove empty day folders
for day_folder in os.listdir(base_folder):
    day_path = os.path.join(base_folder, day_folder)
    if os.path.isdir(day_path) and not os.listdir(day_path):
        os.rmdir(day_path)