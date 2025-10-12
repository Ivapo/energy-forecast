"""
data.py — data loading & preprocessing helpers for energy-forecast

Functions:
- load_raw(path): load the raw CSV into a DataFrame
- preprocess_sweden(df, target_col, benchmark_col, window, threshold): return cleaned df for Sweden
- save_processed(df, out_path): save processed dataframe to CSV
- main(): run as script to load raw, preprocess and save

Usage (script):
    python -m src.energy_forecast.data

Usage (import):
    from src.energy_forecast.data import load_raw, preprocess_sweden, save_processed
"""

from pathlib import Path
import pandas as pd
import numpy as np


# default paths (project-root relative)
RAW_PATH = Path("data/raw/time_series_60min_singleindex.csv")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH = PROCESSED_DIR.joinpath("sweden_processed_hourly.csv")


def load_raw(path: Path | str = RAW_PATH) -> pd.DataFrame:
    """Load the raw CSV into a pandas DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found at {path}. Run data download script first.")
    df = pd.read_csv(path)
    return df


def preprocess_sweden(
    df: pd.DataFrame,
    target_col: str = "SE_load_actual_entsoe_transparency",
    benchmark_col: str = "SE_load_forecast_entsoe_transparency",
    window: int = 12,
    threshold: float = 3.0,
    ) -> pd.DataFrame:
    """
    Preprocess the raw dataframe and return a cleaned Sweden-only DataFrame.
    Steps:
      - select timestamp + target + benchmark
      - parse utc_timestamp -> datetime
      - set datetime index and sort
      - remove duplicate timestamps (keep first)
      - detect missing timestamps and reindex to full hourly index
      - forward-fill then backward-fill missing values
      - detect outliers using a centered rolling window and cap them to mean +/- threshold*std

    Parameters:
      df: raw DataFrame
      target_col: name of the actual load column for Sweden
      benchmark_col: name of the forecast column for Sweden
      window: rolling window size in hours (recommend 6-12)
      threshold: z-score threshold for outlier detection (default 3)

    Returns:
      df_sweden: cleaned pd.DataFrame with datetime index and columns [target_col, benchmark_col]
    """
    # select columns and copy
    cols_needed = ["utc_timestamp", target_col, benchmark_col]
    missing = [c for c in cols_needed if c not in df.columns]
    if missing:
        raise KeyError(f"Missing expected columns in raw data: {missing}")

    df_sweden = df[cols_needed].copy()

    # parse and set index
    print("Parsing timestamps and setting index...")
    df_sweden["utc_timestamp"] = pd.to_datetime(df_sweden["utc_timestamp"])
    df_sweden = df_sweden.set_index("utc_timestamp").sort_index()

    # remove exact duplicate timestamps (keep first)
    print("Checking for duplicate timestamps...")
    if df_sweden.index.duplicated().any():
        print("--> Warning: duplicate timestamps found; removing duplicates.")
        df_sweden = df_sweden[~df_sweden.index.duplicated(keep="first")]
    else:
        print("--> No duplicate timestamps found.")

    # ensure full hourly timeline
    print("Ensuring full hourly timeline...")
    full_index = pd.date_range(start=df_sweden.index.min(), end=df_sweden.index.max(), freq="h")
    missing_count = len(full_index.difference(df_sweden.index))
    if missing_count > 0:
        # reindex (will introduce NaNs for missing timestamps)
        print(f"--> Warning: missing hourly timestamps found; reindexing to full timeline.")
        df_sweden = df_sweden.reindex(full_index)
        df_sweden = df_sweden.sort_index()
        df_sweden.index.name = "utc_timestamp"
    else:
        print("--> No missing timestamps found.")

    # Fill missing values: forward then backward
    print("Filling missing values...")
    df_sweden[target_col] = df_sweden[target_col].ffill().bfill()
    df_sweden[benchmark_col] = df_sweden[benchmark_col].ffill().bfill()

    # simple invalid-value check (non-positive loads)
    print("Correcting invalid values and capping outliers...")
    invalid_mask = df_sweden[target_col] <= 0
    if invalid_mask.any():
        # replace invalid values with local ffill/bfill
        df_sweden.loc[invalid_mask, target_col] = np.nan
        df_sweden[target_col] = df_sweden[target_col].ffill().bfill()

    # outlier detection using centered rolling window
    # rolling with center=True -> local neighborhood
    rolling_mean = df_sweden[target_col].rolling(window=window, center=True, min_periods=1).mean()
    rolling_std = df_sweden[target_col].rolling(window=window, center=True, min_periods=1).std().replace(0, np.nan)  # replace 0 std with NaN to prevent division by zero in next step.

    z_scores = (df_sweden[target_col] - rolling_mean) / rolling_std

    # entries where absolute z > threshold are considered outliers
    outlier_mask = z_scores.abs() > threshold
    if outlier_mask.sum() > 0:
        # cap values at rolling_mean +/- threshold * rolling_std
        signed = np.sign(z_scores).fillna(1)  # +1 or -1
        capped_values = rolling_mean + threshold * rolling_std * signed
        # where outlier_mask True -> replace by capped_values, otherwise keep original
        df_sweden[target_col] = df_sweden[target_col].where(~outlier_mask, capped_values)

    print("Preprocessing complete.")
    return df_sweden

def save_processed(df: pd.DataFrame, out_path: Path | str = PROCESSED_PATH) -> Path:
    """Save processed dataframe to CSV; returns the path."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=True)
    return out_path


def main():
    """Run preprocessing from raw -> processed."""
    print("Loading raw data from CSV...")
    df_raw = load_raw()
    print("Preprocessing Sweden data...")
    df_clean = preprocess_sweden(df_raw)
    saved = save_processed(df_clean)
    print(f"Processed data saved to: {saved}")


if __name__ == "__main__":
    main()
