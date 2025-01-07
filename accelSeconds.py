#adds a seconds column to accelerometer csv file

import pandas as pd
import os

directory = "/Users/nelson/Documents/123F_accel"
all_folders = sorted(os.listdir(directory))
def add_seconds_column(df):
    # Initialize the Seconds column
    seconds = []
    current_second = 0

    # Iterate over the Milliseconds column to determine when the second changes
    for i in range(len(df)):
        if i > 0 and df.loc[i, 'Milliseconds'] < df.loc[i - 1, 'Milliseconds']:
            # Milliseconds decreased, increment the second counter
            current_second += 1
        seconds.append(current_second)

    # Add the Seconds column to the DataFrame
    df['Seconds'] = seconds
    return df

for day_folder in all_folders:
    folder_path = os.path.join(directory, day_folder)
    if os.path.isdir(folder_path):
        for file in sorted(os.listdir(folder_path)):
            if file.endswith(".csv"):
                file_path = os.path.join(folder_path, file)
                try:
                    # Load CSV and add seconds column
                    df = pd.read_csv(file_path, header=0)
                    print(f"Columns in {file}: {df.columns}")

                    # Check if 'Milliseconds' is in the columns
                    if 'Milliseconds' not in df.columns:
                        raise ValueError("'Milliseconds' column not found")

                    df = add_seconds_column(df)

                    # Save the updated DataFrame to the same file (without adding an index column)
                    df.to_csv(file_path, index=False)
                    print(f"Processed file: {file}")
                except Exception as e:
                    print(f"Failed to process {file}: {e}")

