import plotly.express as px
def hourly_heatmap(df):
    g=df.pivot_table(index='day_of_week',columns='hour',values='vehicle_count',aggfunc='mean'); order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']; g=g.reindex([x for x in order if x in g.index]); return px.imshow(g,aspect='auto',color_continuous_scale='Turbo',labels={'color':'Avg Vehicles'})
def scatter_speed(df): return px.scatter(df,x='vehicle_count',y='average_speed',color='congestion_level',hover_data=['location','traffic_density','weather_condition'],color_discrete_map={'Low':'#22c55e','Medium':'#f59e0b','High':'#ef4444'})
def location_bar(df,metric):
    g=df.groupby('location',as_index=False)[metric].mean().sort_values(metric); return px.bar(g,x=metric,y='location',orientation='h',color=metric,color_continuous_scale='Turbo')
