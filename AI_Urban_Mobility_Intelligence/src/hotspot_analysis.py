import pandas as pd
def hotspot_scores(df):
    g=df.groupby('location').agg(vehicle_count=('vehicle_count','mean'),average_speed=('average_speed','mean'),traffic_density=('traffic_density','mean'),accident_count=('accident_count','sum'),congestion_rate=('congestion_level',lambda s:(s=='High').mean()),road_capacity=('road_capacity','mean')).reset_index()
    def norm(s):
        lo,hi=s.min(),s.max(); return (s-lo)/(hi-lo) if hi>lo else pd.Series(.5,index=s.index)
    g['speed_reduction']=1-norm(g.average_speed)
    g['hotspot_score']=(100*(.24*norm(g.vehicle_count)+.24*norm(g.traffic_density)+.22*g.congestion_rate+.12*norm(g.accident_count)+.10*g.speed_reduction+.08*norm(g.vehicle_count/g.road_capacity))).round(1)
    g['risk']=pd.cut(g.hotspot_score,[-1,33.33,66.66,101],labels=['Low Risk','Moderate Risk','High Risk'])
    return g.sort_values('hotspot_score',ascending=False).reset_index(drop=True)
