import sys
import json
import pandas as pd
 
 
def distribution_summary(df: pd.DataFrame):
    """
    Compute distribution metrics for numeric and categorical columns.
 
    Numeric metrics:
      - count
      - missing_percent
      - mean, median, std
      - min, 25%, 75%, max
      - skewness, kurtosis
      - outlier count (1.5*IQR rule)
 
    Categorical metrics:
      - count
      - missing_percent
      - unique values
      - top category and its frequency
 
    Returns:
      numeric_stats (DataFrame), categorical_stats (DataFrame)
    """
    numeric = df.select_dtypes(include=["number"])
    categorical = df.select_dtypes(include=["object", "category"])
 
    numeric_stats = pd.DataFrame({
        "count": numeric.count(),
        "missing_percent": numeric.isnull().mean() * 100,
        "mean": numeric.mean(),
        "median": numeric.median(),
        "std": numeric.std(),
        "min": numeric.min(),
        "25%": numeric.quantile(0.25),
        "75%": numeric.quantile(0.75),
        "max": numeric.max(),
        "skewness": numeric.skew(),
        "kurtosis": numeric.kurt()
    })
 
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outlier_count = ((numeric < lower) | (numeric > upper)).sum()
    numeric_stats["outlier_count"] = outlier_count
 
    cat_stats = pd.DataFrame({
        "count": categorical.count(),
        "missing_percent": categorical.isnull().mean() * 100,
        "unique": categorical.nunique(),
        "top": categorical.mode().iloc[0],
        "top_freq": categorical.value_counts().iloc[0]
    })
 
    return numeric_stats, cat_stats
 
 
def load_config(path: str):
    with open(path, 'r') as f:
        return json.load(f)
 
 
def main():
    # Determine mode: JSON config or interactive
    if len(sys.argv) == 2 and sys.argv[1].lower().endswith('.json'):
        cfg = load_config(sys.argv[1])
        data_path = cfg.get('input')
        num_out = cfg.get('numeric_output', 'numeric_distribution_summary.csv')
        cat_out = cfg.get('categorical_output', 'categorical_distribution_summary.csv')
    else:
        data_path = input("Enter full path to the dataset CSV: ").strip()
        num_out = input("Enter path for numeric summary output (or press Enter for default 'numeric_distribution_summary.csv'): ").strip() or 'numeric_distribution_summary.csv'
        cat_out = input("Enter path for categorical summary output (or press Enter for default 'categorical_distribution_summary.csv'): ").strip() or 'categorical_distribution_summary.csv'
 
    try:
        df = pd.read_csv(data_path)
        print(f"Loaded dataset: {data_path} (shape: {df.shape})")
    except Exception as e:
        print(f"Error reading dataset: {e}")
        sys.exit(1)
 
    numeric_stats, categorical_stats = distribution_summary(df)
 
    print("\nNumeric Distribution Summary:")
    print(numeric_stats.to_string())
    print("\nCategorical Distribution Summary:")
    print(categorical_stats.to_string())
 
    numeric_stats.to_csv(num_out)
    categorical_stats.to_csv(cat_out)
    print(f"\nSummary files written:\n - {num_out}\n - {cat_out}")
 
 
if __name__ == '__main__':
    main()
