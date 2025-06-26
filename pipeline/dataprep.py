import sys
import json
import pandas as pd
 
def merge_csv_files():
    """
    Prompts for full CSV file paths, merges them vertically into one DataFrame,
    and optionally saves the result.
    """
    print("STEP 1: Merge multiple CSV files")
    print("Enter the full paths to each CSV you want to merge.")
    print(" - You can separate them with commas")
    print(" - Or enter one per line (finish by pressing Enter on an empty line)")
    first = input().strip()
    # Build list of paths
    if "," in first:
        paths = [p.strip() for p in first.split(",") if p.strip()]
    else:
        paths = [first] if first else []
        while True:
            line = input().strip()
            if not line:
                break
            paths.append(line)
    if not paths:
        print("No files provided. Exiting.")
        raise SystemExit
    dataframes = []
    for path in paths:
        try:
            df = pd.read_csv(path)
            dataframes.append(df)
            print(f"Loaded file: {path} (shape: {df.shape})")
        except FileNotFoundError:
            print(f"File not found: {path}")
        except Exception as e:
            print(f"Error reading {path}: {e}")
    if not dataframes:
        print("No CSV files could be loaded. Exiting.")
        raise SystemExit
    merged = pd.concat(dataframes, ignore_index=True)
    print(f"Merged {len(dataframes)} files. Combined shape: {merged.shape}")
    save_path = input("Enter full path to save merged quotes CSV (or press Enter to skip): ").strip()
    if save_path:
        merged.to_csv(save_path, index=False)
        print(f"Merged quotes saved to: {save_path}")
    return merged
 
def merge_vehicle_into_quote(df_quote):
    """
    Prompts for the vehicle CSV path and ABI column names, then
    inner-joins vehicle data into the quote DataFrame on ABI.
    """
    print("\nSTEP 2: Merge vehicle data into quotes")
    vehicle_path = input("Enter full path to the vehicle CSV: ").strip()
    try:
        df_vehicle = pd.read_csv(vehicle_path)
        print(f"Loaded vehicle data: {vehicle_path} (shape: {df_vehicle.shape})")
    except Exception as e:
        print(f"Could not read vehicle file: {e}")
        raise SystemExit
    abi_quote_col = input("Enter the ABI column name in the quote data: ").strip()
    abi_vehicle_col = input("Enter the ABI column name in the vehicle data: ").strip()
    # Ensure both are strings to match numeric/text codes
    df_quote[abi_quote_col]     = df_quote[abi_quote_col].astype(str)
    df_vehicle[abi_vehicle_col] = df_vehicle[abi_vehicle_col].astype(str)
    merged = pd.merge(
        df_quote,
        df_vehicle,
        left_on=abi_quote_col,
        right_on=abi_vehicle_col,
        how='inner'
    )
    print(f"Inner join complete on '{abi_quote_col}' / '{abi_vehicle_col}'. Resulting shape: {merged.shape}")
    save_path = input("Enter full path to save final merged CSV (or press Enter to skip): ").strip()
    if save_path:
        merged.to_csv(save_path, index=False)
        print(f"Final merged dataset saved to: {save_path}")
    return merged
 
def main():
    # JSON configuration mode
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
        print(f"Loading configuration from: {config_path}")
        with open(config_path, 'r') as f:
            cfg = json.load(f)
        # Merge quotes
        quote_files = cfg['quotes']['files']
        merged_quotes = pd.concat(
            [pd.read_csv(p) for p in quote_files],
            ignore_index=True
        )
        print(f"Loaded {len(quote_files)} quote files. Combined shape: {merged_quotes.shape}")
        if cfg['quotes'].get('output'):
            merged_quotes.to_csv(cfg['quotes']['output'], index=False)
            print(f"Merged quotes saved to: {cfg['quotes']['output']}")
        # Merge vehicle
        vehicle_cfg = cfg['vehicle']
        df_vehicle = pd.read_csv(vehicle_cfg['file'])
        print(f"Loaded vehicle data. Shape: {df_vehicle.shape}")
        qcol = vehicle_cfg['abi_quote_col']
        vcol = vehicle_cfg['abi_vehicle_col']
        merged_quotes[qcol]   = merged_quotes[qcol].astype(str)
        df_vehicle[vcol]      = df_vehicle[vcol].astype(str)
        final = pd.merge(
            merged_quotes,
            df_vehicle,
            left_on=qcol,
            right_on=vcol,
            how='inner'
        )
        print(f"Inner join on '{qcol}' / '{vcol}' complete. Resulting shape: {final.shape}")
        if vehicle_cfg.get('output'):
            final.to_csv(vehicle_cfg['output'], index=False)
            print(f"Final merged dataset saved to: {vehicle_cfg['output']}")
        return final
 
    # Interactive mode
    quotes_df = merge_csv_files()
    final_df  = merge_vehicle_into_quote(quotes_df)
    print("Data preparation complete.")
    return final_df
 
if __name__ == "__main__":
    main()
