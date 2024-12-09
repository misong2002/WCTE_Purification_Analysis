# Purification System Analysis

This repository contains data and analysis related to the purification system. It includes raw data from the purification system, logs of system operations, and Jupyter Notebook scripts for analyzing and visualizing the data.

## Dependence
Python 3.12.3
Matplotlib 3.9.3


## Repository Structure

- `analysis/`: Contains Jupyter Notebooks (`.ipynb`) for data analysis and visualization.
- `data/`: Raw data files from the purification system, collected from October 18 to November 27. (`test.csv` only contains 1-hour data. The full data file `merged.csv` can be found from:
- `logging.txt`: Log file containing records of the purification system's operations during the data collection period.


## How to Use the Repository

1. Clone the repository:
   ```bash
   git clone https://github.com/misong2002/WCTE_Purification_Analysis.git

2. Build data file
   ```bash
   make

3.Run the scripts in `analysis/`