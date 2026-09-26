from pathlib import Path
import json, py_compile
ROOT=Path(__file__).resolve().parent
required=["app.py","requirements.txt","README.md","data/raw/traffic_raw.csv","data/processed/traffic_cleaned.csv","models/congestion_model.pkl","models/model_metadata.json","notebooks/traffic_exploration.ipynb"]
missing=[x for x in required if not (ROOT/x).exists()]
if missing: raise SystemExit("Missing: "+", ".join(missing))
for p in ROOT.rglob("*.py"): py_compile.compile(str(p),doraise=True)
import pandas as pd
df=pd.read_csv(ROOT/"data/processed/traffic_cleaned.csv")
meta=json.loads((ROOT/"models/model_metadata.json").read_text())
assert len(df)>=10000 and df.isna().sum().sum()==0
assert set(df.congestion_level)=={"Low","Medium","High"}
assert meta.get("feature_importance")
print(f"Records: {len(df):,}")
print(f"Selected model: {meta['selected_model']}")
print("Python syntax: PASS")
print("Core files: PASS")
try:
 import streamlit, plotly, folium, streamlit_folium
 print("Dashboard dependencies: PASS")
except Exception as e:
 print("Dashboard dependencies: install from requirements.txt before running (not installed in this environment):",e)
print("Project verification complete.")
