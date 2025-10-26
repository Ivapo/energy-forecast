# ⚡ Energy Forecasting Project


This project showcases **data science and time series forecasting skills** using `Open Power System Data`. 
It demonstrates a full workflow from data acquisition to forecasting, organized code, and deployment.

---

## 📋 Project Overview

- **Goal:** Forecast short-term electricity demand (hourly) in Sweden.  
- **Purpose:** Accurate demand forecasting helps energy providers balance the grid, optimize renewable integration, and support decision-making.  
- **Dataset:** Open Power System Data — Hourly electricity load, wind and solar generation, and related variables.  
- **Scope:** Includes scripts for downloading data, preprocessing, feature engineering, model training, and visualization.

---

## 🧩 Purpose 

The goal of the `energy-forecast` project is to **forecast short-term (hourly) electricity demand in Sweden** using historical time series data from Open Power System Data.

### Objectives
- **Load and preprocess** hourly electricity load, wind and solar generation, and related variables.
- **Explore and visualize** patterns, trends, and missing values.
- **Engineer features** suitable for forecasting, including lag features, rolling averages, and time-based features.
- **Build forecasting models** using tools like Prophet or scikit-learn regressors.
- **Generate predictions** and visualize results.
- **(Optional) Deploy a minimal API** using FastAPI to serve forecasts.

### Motivation
Accurate demand forecasting helps energy providers:
- Balance the electricity grid
- Optimize renewable energy integration
- Support operational and strategic decision-making

This project demonstrates **end-to-end data science skills**: 

> **Data acquisition & preprocessing → EDA → Feature engineering → Modeling → Deployment**

## ⚙️ Workflow

### Dataset : Open Power System Data - [<u>data.open-power-system-data.org</u>](https://data.open-power-system-data.org/time_series/)  

Download the data by running:

```
uv run python -m src.energy_forecast.download_data
```

Data is downloaded to: `data/raw/time_series_60min_singleindex.csv`

### Preprocess Data


```
uv run python -m src.energy_forecast.data
```

This runs `src/energy_forecast/data.py` which preprocess the  `time_series_60min_singleindex.csv` file and saves cleaned data to: `data/processed/sweden_processed_hourly.csv`
- selection of columns for Sweden : actual energy load (`SE_load_actual_entsoe_transparency`) and forecasted load for benchmarking (`SE_load_forecast_entsoe_transparency`)
- parsing `utc_timestamp` column and setting as datetime index
- invalid-value handling (non-positive loads)
- removal of duplicate timestamps
- reindexing to a complete hourly range (if any timestamps missing)
- forward-fill then backward-fill for missing values
- rolling-window outlier detection and capping (centered window, 12 hour window, threshold of 3 std)
- saves preprocessed data to `data/processed/sweden_processed_hourly.csv`

### Exploratory Data Analysis

## ⚙️ Project Setup

### 1. Clone repository

```bash
git clone https://github.com/ivapo/energy-forecast.git
cd energy-forecast
```

### 2. Setup UV environment

* Create virtual environment and install dependencies
* Create kernel for notebooks `Python (energy-forecast)`

```bash
uv init
uv sync
uv run python -m ipykernel install --user --name=energy-forecast --display-name "Python (energy-forecast)"
```

## 🗂 Project Structure

```bash
energy-forecast/
├── data/
│   ├── raw/           # Original CSV downloaded by script
│   └── processed/     
├── notebooks/
│   ├── 00_data_preprocessing.ipynb
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

- [Open Power System Data](https://data.open-power-system-data.org/time_series/)  










