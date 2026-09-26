import pandas as pd
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from config.config import RAW_DATA,PROCESSED_DATA
REQUIRED=['record_id','timestamp','date','time','day_of_week','hour','location','latitude','longitude','road_type','road_capacity','vehicle_count','average_speed','traffic_density','occupancy_rate','weather_condition','temperature','rainfall','visibility','accident_count','congestion_level']
def clean_data(df):
    missing=[c for c in REQUIRED if c not in df.columns]
    if missing: raise ValueError(f'Missing columns: {missing}')
    df=df.copy().drop_duplicates('record_id'); df['timestamp']=pd.to_datetime(df['timestamp'],errors='coerce'); df=df.dropna(subset=['timestamp','location','congestion_level'])
    nums=['latitude','longitude','road_capacity','vehicle_count','average_speed','traffic_density','occupancy_rate','temperature','rainfall','visibility','accident_count','hour']
    for c in nums: df[c]=pd.to_numeric(df[c],errors='coerce')
    df=df.dropna(subset=nums); df['hour']=df['hour'].astype(int).clip(0,23); df['rainfall']=df['rainfall'].clip(lower=0); df['visibility']=df['visibility'].clip(1,10); df['average_speed']=df['average_speed'].clip(1,120); df['vehicle_count']=df['vehicle_count'].clip(lower=0); df['traffic_density']=df['traffic_density'].clip(lower=0)
    df['date']=df.timestamp.dt.date.astype(str); df['time']=df.timestamp.dt.strftime('%H:%M'); df['day_of_week']=df.timestamp.dt.day_name()
    return df.sort_values('timestamp').reset_index(drop=True)
if __name__=='__main__':
    if not RAW_DATA.exists():
        from data_generation import generate_data; generate_data()
    out=clean_data(pd.read_csv(RAW_DATA)); PROCESSED_DATA.parent.mkdir(parents=True,exist_ok=True); out.to_csv(PROCESSED_DATA,index=False); print(f'Saved {len(out):,} cleaned records')
