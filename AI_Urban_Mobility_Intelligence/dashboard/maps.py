import folium
from folium.plugins import MarkerCluster
def traffic_map(df,scores):
    m=folium.Map(location=[df.latitude.mean(),df.longitude.mean()],zoom_start=12,tiles='CartoDB dark_matter'); cluster=MarkerCluster().add_to(m); lookup=dict(zip(scores.location,scores.risk.astype(str)))
    for _,r in df.drop_duplicates('location').iterrows():
        risk=lookup.get(r.location,'Moderate Risk'); color={'Low Risk':'green','Moderate Risk':'orange','High Risk':'red'}.get(risk,'blue'); x=df[df.location==r.location]
        popup=f"<b>{r.location}</b><br>Risk: {risk}<br>Avg vehicles: {x.vehicle_count.mean():.0f}<br>Avg speed: {x.average_speed.mean():.1f} km/h"
        folium.CircleMarker([r.latitude,r.longitude],radius=10,color=color,fill=True,fill_opacity=.85,popup=folium.Popup(popup,max_width=280)).add_to(cluster)
    return m
