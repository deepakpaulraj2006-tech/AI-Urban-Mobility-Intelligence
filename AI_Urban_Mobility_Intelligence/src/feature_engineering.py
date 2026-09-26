import pandas as pd
def engineer_features(df):
    out=df.copy(); ts=pd.to_datetime(out.timestamp); out['is_weekend']=(ts.dt.dayofweek>=5).astype(int); out['is_peak_hour']=(((out.hour>=7)&(out.hour<=10))|((out.hour>=17)&(out.hour<=20))).astype(int); out['capacity_utilization']=out.vehicle_count/out.road_capacity.replace(0,1); out['speed_ratio']=out.average_speed/80; return out
