<!-- File: README_data_prep.md -->
# README for Data Preparation Script (`dataprep.py`)
 
## Overview
 
`data_prep.py` is a Python utility to merge multiple quote CSV files and integrate vehicle data, keyed by ABI codes, producing a final merged dataset.
 
## Prerequisites
 
- Python 3.7 or higher
- `pandas` library: Install via `pip install pandas`
 
## Files
 
- `data_prep.py`: Main script
- `config.json` (optional): JSON configuration for non-interactive mode
 
## Usage
 
### 1. Interactive Mode
 
Run the script without arguments to supply inputs via prompts:
 
```bash
python data_prep.py
```
 
**Prompts:**
1. Full paths to quote CSVs (comma-separated or one-per-line)
2. Optional output path for merged quotes
3. Full path to vehicle CSV
4. ABI column name in quote data
5. ABI column name in vehicle data
6. Optional output path for final merge
 
### 2. JSON Configuration Mode
 
Create a `config.json` file with the structure:
 
```json
{
  "quotes": {
    "files": ["/path/to/quote1.csv", "/path/to/quote2.csv"],
    "output": "/path/to/merged_quotes.csv"
  },
  "vehicle": {
    "file": "/path/to/vehicles.csv",
    "abi_quote_col": "QuoteABI",
    "abi_vehicle_col": "VehABI",
    "output": "/path/to/final_merged.csv"
  }
}
```
 
Run with:
 
```bash
python data_prep.py config.json
```
 
## Output
 
- Merged quotes CSV (if `output` specified)
- Final merged dataset CSV (if `output` specified)
 
---

<!-- File: README_distribution_checker.md -->
# README for Distribution Checker (`distribution checker.py`)
 
## Overview
 
`distribution_checker.py` computes and reports distribution metrics for numeric and categorical features in a dataset, optionally via JSON configuration.
 
## Prerequisites
 
- Python 3.7 or higher
- `pandas` library: Install via `pip install pandas`
 
## Files
 
- `distribution_checker.py`: Main script
- `config.json` (optional): JSON configuration for non-interactive mode
 
## Usage
 
### 1. Interactive Mode
 
Run the script without arguments:
 
```bash
python distribution_checker.py
```
 
**Prompts:**
1. Dataset CSV path
2. Optional path for numeric summary output (default: `numeric_distribution_summary.csv`)
3. Optional path for categorical summary output (default: `categorical_distribution_summary.csv`)
 
### 2. JSON Configuration Mode
 
Create a `config.json` file with the structure:
 
```json
{
  "input": "/path/to/dataset.csv",
  "numeric_output": "/path/to/numeric_summary.csv",
  "categorical_output": "/path/to/categorical_summary.csv"
}
```
 
Run with:
 
```bash
python distribution_checker.py config.json
```
 
## Metrics Computed
 
**Numeric Features:** count, missing %, mean, median, standard deviation, min/25%/75%/max, skewness, kurtosis, outlier count (1.5×IQR)
 
**Categorical Features:** count, missing %, unique values, top category, and its frequency
 
## Output
 
- `numeric_distribution_summary.csv`
- `categorical_distribution_summary.csv`
