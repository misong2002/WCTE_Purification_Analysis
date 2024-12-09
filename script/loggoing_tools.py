import numpy as np
import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def read_csv_to_dict(csv_filename):
    # Reads a CSV file into a dictionary with column names as keys and column data as NumPy arrays
    df = pd.read_csv(csv_filename)
    columns_dict = {col: np.array(df[col]) for col in df.columns}
    return columns_dict


def calculate_seconds(date_list, time_list):
    # Fixed target time ("03-10-2024 17:00:00")
    target_time_str = "03-10-2024 17:00:00"
    target_time = datetime.strptime(target_time_str, "%d-%m-%Y %H:%M:%S")
    
    # List to store the difference in seconds
    seconds_list = []
    
    # Iterate through the date and time arrays
    for date_str, time_str in zip(date_list, time_list):
        # Combine date and time into a single string and convert to datetime
        input_time_str = f"{date_str} {time_str}"
        input_time = datetime.strptime(input_time_str, "%d-%m-%Y %H:%M:%S")
        
        # Calculate the time difference in seconds
        delta = input_time - target_time
        seconds = delta.total_seconds()
        
        # Append the seconds to the list
        seconds_list.append(int(seconds))
    
    return seconds_list


def find_falling_edge_index(time_and_date, Flow, target_value=1.5):
    # Detects falling edges in the Flow data where the value is close to target_value
    # A falling edge occurs when the previous value > target_value, current value == target_value, and next value < target_value
    indices = []
    skip_count = 0  # Skip indices to avoid redundant edge detection

    for i in range(1, Flow.shape[0] - 1):
        if skip_count > 0:
            skip_count -= 1
            continue
        if np.abs(Flow[i] - target_value) < 0.1:
            indices.append(i)
            skip_count = 300  # Skip the next 300 indices to prevent redundancy

    # Retrieve corresponding time_and_date values
    time_and_date_values = time_and_date[indices]
    return time_and_date_values


def initialize_event_list(time_and_date, columns_dict):
    # Initialize an event list based on detected falling edges
    auto_event_time = find_falling_edge_index(time_and_date, columns_dict["FT1_Flow"], target_value=2)

    with open('./logging.txt', 'w') as f:
        for item in auto_event_time:
            # Split time and date, then format and write to file
            time, date = item.split()
            f.write(f"{time},{date},\n")
    
    return 0


def read_event_list(file_path):
    # Reads the event list from a file and converts it into a NumPy array
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip().split(','))  # Remove newline and split by comma

    # Convert list to a NumPy array (n x 2)
    array = np.array(lines).T
    return array


def plot_data(data_dict, columns_dict, time_range, date_range,seconds_from_start, value_plot_range, event_list):
    # Converts start and end time to datetime
    second_range = np.array(calculate_seconds(date_range, time_range), dtype=int)
    title = [
        "PT3 level (m) or True/False",
        "True/False",
        "Flow (t/h) or Pressure (bar)",
        "Conductivity (uS/cm)",
        "Level (m)",
        "Conductivity (uS/cm)\n or TDS (mg/L)\n or Salinity (PSU)",
        "Temperature (°C)"
    ]
    
    fig, axes = plt.subplots(7, 1, figsize=(15, 15))
    axes = axes.flatten()  # Flatten to a 1D array for easy iteration
    
    event_seconds = np.array(calculate_seconds(event_list[1], event_list[0]), dtype=int)

    # Filter data based on time range
    mask = (seconds_from_start >= second_range[0]) & (seconds_from_start <= second_range[1])
    event_mask = (event_seconds >= second_range[0]) & (event_seconds <= second_range[1])

    filtered_second = seconds_from_start[mask]
    filtered_event_hours = (event_seconds[event_mask] - second_range[0]) / 3600
    time_scale = (filtered_second - second_range[0]) / 3600
    filtered_event_name = event_list[2][event_mask]

    # Plot data for each group
    for i, (key, sub_dict) in enumerate(data_dict.items()):
        ax = axes[i]
        group_keys = list(sub_dict)
        
        # Plot data for each key in the group
        for group_key in group_keys:
            if group_key in columns_dict:
                value_data = columns_dict[group_key]
                filtered_values = value_data[mask]
                ax.plot(time_scale, filtered_values, label=group_key)

        # Add event markers if applicable
        if filtered_event_name.shape[0] != 0:
            ax.vlines(filtered_event_hours, *value_plot_range[i], colors='r', linestyle="--")

        # Configure plot labels and settings
        ax.set_xlim(0, (second_range[1] - second_range[0]) / 3600)
        ax.set_ylabel(title[i])
        ax.set_ylim(*value_plot_range[i])
        ax.legend()
        ax.grid(True)

    last_ax = axes[-1]  # Last subplot for adding time labels
    last_ax.set_xlabel("Time (h)")
    
    fig.text(-0.03, -1.2, f"{time_range[0]} {date_range[0]}",
             transform=last_ax.transAxes, fontsize=10, ha='left', va='bottom', color='black', rotation=90)
    fig.text(1.03, -1.2, f"{time_range[1]} {date_range[1]}",
             transform=last_ax.transAxes, fontsize=10, ha='right', va='bottom', color='black', rotation=90)

    for hour, time, date, name in zip(filtered_event_hours, event_list[0][event_mask], event_list[1][event_mask], filtered_event_name):
        fig.text(hour / ((second_range[-1] - second_range[0]) / 3600), -1.2, f"{time} {date}",
                 transform=last_ax.transAxes, fontsize=10, ha='right', va='bottom', color='black', rotation=90)
        fig.text(hour / ((second_range[-1] - second_range[0]) / 3600), 8.7, f"{name}",
                 transform=last_ax.transAxes, fontsize=10, ha='right', va='bottom', color='black', rotation=90)

    plt.tight_layout()
    plt.show()
