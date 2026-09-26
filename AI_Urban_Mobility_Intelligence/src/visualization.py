import plotly.express as px
def congestion_distribution(df): return px.histogram(df,x='congestion_level',color='congestion_level')
def hourly_traffic(df): return px.line(df.groupby('hour',as_index=False).vehicle_count.mean(),x='hour',y='vehicle_count',markers=True)
