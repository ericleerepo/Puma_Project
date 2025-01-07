#splits daily accelerometer csv into seperate csv per hour

import pandas as pd
import os

# Load the CSV file into a DataFrame
directory = "/Users/nelson/Documents/123F_accel"
all_folders = sorted(os.listdir(directory))
for day_folder in all_folders:
    folder_path = os.path.join(directory, day_folder)
    if os.path.isdir(folder_path):
        files = os.listdir(folder_path)
        file_name = files[0]
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, header=1)
        print(df.columns)
        print(file_name)

        date = os.path.splitext(file_name)[0]

        # Combine date and time if necessary (assuming 'UTC DateTime' is time and the date is separate)
        df['FullDatetime'] = pd.to_datetime(date + " " + df['UTC DateTime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

        # Set the FullDatetime as the DataFrame index
        df.set_index('FullDatetime', inplace=True)

        # Group by hour
        hourly_groups = df.groupby(df.index.hour)

        # Save each group to a separate file
        for hour, group in hourly_groups:
            output_filename = os.path.join(folder_path, date+f"-{hour:02d}.csv")
            group.to_csv(output_filename)
            print(f"Saved data for hour {hour} to file {output_filename}")
        os.remove(file_path)
        print("Files have been created.")