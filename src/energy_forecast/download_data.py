import os
import requests

# URL of the Open Power System Data CSV (hourly data)
DATA_URL="https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv"

# Local path to save the CSV
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/raw")
RAW_DATA_FILE = os.path.join(RAW_DATA_DIR, "time_series_60min_singleindex.csv")

def download_data(url=DATA_URL, dest=RAW_DATA_FILE):
    """Download CSV from URL and save to data/raw folder."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    
    if os.path.exists(dest):
        print(f"Data already exists at {dest}")
        return

    print(f"Downloading data from {url} ...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Download complete! Saved to {dest}")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")

if __name__ == "__main__":
    download_data()
