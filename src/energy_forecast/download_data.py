"""
download_data.py — download raw CSV data for energy-forecast

Usage (script):
    python -m src.energy_forecast.download_data

Usage (import):
    from src.energy_forecast.download_data import download_raw_csv
"""

from pathlib import Path
import requests

# Paths
RAW_DIR = Path("data").joinpath("raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
RAW_PATH = RAW_DIR.joinpath("time_series_60min_singleindex.csv")

# URL of the Open Power System Data CSV (hourly data)
DATA_URL="https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv"

def download_raw_csv(url=DATA_URL, dest=RAW_PATH):
    """
    Download CSV from URL and save to data/raw folder.
    """

    print(f"Downloading raw data from {url} ...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Download complete! Saved to {dest}")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")
    return dest



def main():
    download_raw_csv()


if __name__ == "__main__":
    main()