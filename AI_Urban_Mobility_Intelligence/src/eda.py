def summary(df): return {'rows':len(df),'columns':len(df.columns),'missing_values':int(df.isna().sum().sum())}
def hourly_profile(df): return df.groupby('hour',as_index=False).agg(vehicle_count=('vehicle_count','mean'),average_speed=('average_speed','mean'))
