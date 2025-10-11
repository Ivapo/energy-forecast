# ⚡ Energy Forecasting Project

This project showcases **data science and time series forecasting skills** using open electricity load data for Sweden. It demonstrates a full workflow from data acquisition to forecasting, organized code, and optional deployment.

---

## 📋 Project Overview

- **Goal:** Forecast short-term electricity demand (hourly) in Sweden.  
- **Purpose:** Accurate demand forecasting helps energy providers balance the grid, optimize renewable integration, and support decision-making.  
- **Dataset:** Open Power System Data — Hourly electricity load, wind and solar generation, and related variables.  
- **Scope:** Includes scripts for downloading data, preprocessing, feature engineering, model training, and visualization.  

## ⚙️ Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/energy-forecast.git
cd energy-forecast
```

### 2. Initialize UV environment

```bash
uv init
```
* Creates an isolated virtual environment and `pyproject.toml`

### 3. Install dependencies

```bash
uv sync
```

* Installs all dependencies

## 📥 Download Dataset

The project uses the **Open Power System Data** CSV. 
Download it running:

```bash
uv run python src/energy_forecast/download_data.py
```

* The data will be downloaded, avoiding duplication, to: `data/raw/time_series_60min_singleindex.csv`


## 🗂 Project Structure

```bash
energy-forecast/
├── data/
│   ├── raw/           # Original CSV downloaded by script
│   └── processed/     # Preprocessed data for modeling
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_feature_engineering_and_modeling.ipynb
├── src/
│   └── energy_forecast/
│       ├── __init__.py
│       ├── data.py
│       ├── features.py
│       ├── train.py
│       ├── predict.py
│       └── download_data.py
├── models/                 # Model artifacts (gitignored)
├── results/                # Output figures, CSVs, reports
├── Dockerfile              # Containerize project for deployment
├── pyproject.toml          # uv dependencies
├── .gitignore
└── README.md
```

## 🚀 Usage Instructions

### 1. Explore data

Open `notebooks/01_data_exploration.ipynb` and examine the dataset, visualize load trends, and detect seasonality and anomalies.  

### 2. Preprocess and engineer features

Use `notebooks/02_feature_engineering_and_modeling.ipynb` or functions in `src/energy_forecast/features.py` to:

- Create lag features, rolling averages, and time-based variables (hour, weekday, month).  

### 3. Train model

```bash
uv run python src/energy_forecast/train.py
```

* Trains a forecasting model and saves it to `models/`

### 4. Make predictions

```bash
uv run python src/energy_forecast/predict.py
```
* Loads the model and outputs forecasts.

### 5. Optional: Containerized deployment

```bash
docker build -t energy-forecast .
docker run -p 8000:8000 energy-forecast
```
* Exposes a `FastAPI` app or dashboard (if implemented).

## 🧰 Tech Stack

- Python 3.10+  
- Pandas / NumPy  
- Matplotlib / Seaborn / Plotly  
- Scikit-learn  
- Prophet (for time series forecasting)  
- FastAPI + Uvicorn (optional deployment)  
- uv (Python package management)  

---

## 🔍 Future Work

- Integrate weather and renewable generation as exogenous variables.  
- Experiment with advanced forecasting models (LSTM, Transformers).  
- Add interactive dashboards using Streamlit or Dash.  
- Implement automated batch forecast pipelines with Docker.  

---

## 📄 References

- [Open Power System Data](https://data.open-power-system-data.org/)  










