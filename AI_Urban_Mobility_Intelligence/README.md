# AI Urban Mobility Intelligence System

## Data-Driven Traffic Analysis, Hotspot Detection & Congestion Prediction

A polished academic Smart-City traffic intelligence prototype combining simulated traffic data, exploratory data analysis, geospatial hotspot analysis, multiclass machine learning and an interactive Streamlit dashboard.

## Quick Start (Windows / VS Code)

Open this folder in VS Code and run:

```bash
pip install -r requirements.txt
python src/data_generation.py
python src/data_cleaning.py
python src/train_model.py
streamlit run app.py
```

Or double-click `RUN_PIPELINE.bat` to regenerate the data, clean it, train the model and run verification. Then double-click `START_DASHBOARD.bat`.

## Dashboard Pages

- Overview — premium KPI cards, traffic status, trends and automated insights
- Traffic Analytics — filters, day/hour heatmap, scatter analysis, weather and road comparisons
- Hotspot Intelligence — project-defined hotspot score, risk table and interactive Folium map
- Congestion Prediction — actual saved ML model with probability visualization
- Model Insights — model metrics, confusion matrix and permutation feature importance
- What-If Simulator — baseline vs modified model-based scenario comparison
- About Project — scope, technology and limitations

## Project pipeline

DATA → CLEANING → FEATURE ENGINEERING → EDA → HOTSPOTS → ML → DASHBOARD → PREDICTION → WHAT-IF

## Dataset

15,000 reproducible simulated traffic records across ten fictional academic locations. The dataset includes temporal, road, vehicle, speed, density, weather, rainfall, visibility and accident variables.

The data is **simulated for academic demonstration**. Locations are fictional/simulated. It must not be presented as real government, sensor or live traffic data.

## Machine Learning

The project compares Logistic Regression, Decision Tree and Random Forest using a stratified train/test split. Metrics include Accuracy, weighted Precision, weighted Recall, weighted F1 and a confusion matrix. The deployment model is selected by highest weighted F1, with accuracy as the secondary criterion.

## Hotspot score

The hotspot score combines normalized traffic volume, density, high-congestion rate, accident frequency, speed reduction and capacity utilization. It is a **project-defined academic indicator**, not an official traffic-authority formula.

## Verification

Run:

```bash
python verify_project.py
python -m pytest -q
```

`verify_project.py` checks core files, Python syntax, dataset size/quality, model metadata and dashboard dependency availability.

## Limitations and future scope

This prototype does not provide real-time traffic forecasting. A production system would require validated GPS/sensor feeds, real geographic locations, monitoring, model retraining, data governance and operational validation.
