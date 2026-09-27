import folium
from folium.plugins import MarkerCluster


def traffic_map(df, scores):

    # Remove records without valid coordinates
    map_df = df.dropna(subset=["latitude", "longitude"]).copy()

    # Default map location
    if map_df.empty:
        m = folium.Map(
            location=[9.9252, 78.1198],
            zoom_start=12,
            tiles="OpenStreetMap"
        )
        folium.Marker(
            [9.9252, 78.1198],
            popup="No valid location data available"
        ).add_to(m)
        return m

    # Create map
    m = folium.Map(
        location=[
            map_df["latitude"].mean(),
            map_df["longitude"].mean()
        ],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # Risk lookup
    lookup = dict(
        zip(
            scores["location"],
            scores["risk"].astype(str)
        )
    )

    # Marker cluster
    cluster = MarkerCluster(
        name="Traffic Hotspots"
    ).add_to(m)

    # Add hotspot markers
    for _, r in map_df.drop_duplicates("location").iterrows():

        location = r["location"]
        risk = lookup.get(location, "Moderate Risk")

        color_map = {
            "Low Risk": "green",
            "Moderate Risk": "orange",
            "High Risk": "red"
        }

        color = color_map.get(risk, "blue")

        location_data = map_df[
            map_df["location"] == location
        ]

        avg_vehicles = location_data["vehicle_count"].mean()
        avg_speed = location_data["average_speed"].mean()

        popup_html = f"""
        <div style="font-family:Arial; width:220px;">
            <h4 style="margin-bottom:8px;">
                📍 {location}
            </h4>

            <b>Risk:</b>
            <span style="color:{color};">
                {risk}
            </span>

            <br><br>

            <b>🚗 Avg Vehicles:</b>
            {avg_vehicles:.0f}

            <br>

            <b>⚡ Avg Speed:</b>
            {avg_speed:.1f} km/h
        </div>
        """

        folium.CircleMarker(
            location=[
                r["latitude"],
                r["longitude"]
            ],
            radius=12,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            weight=3,
            popup=folium.Popup(
                popup_html,
                max_width=300
            ),
            tooltip=f"📍 {location} — {risk}"
        ).add_to(cluster)

    # Map legend
    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        width: 170px;
        background: white;
        border: 2px solid #cccccc;
        z-index: 9999;
        padding: 12px;
        font-size: 13px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    ">
        <b>🔥 Congestion Risk</b><br><br>

        <span style="color:green;">●</span>
        Low Risk<br>

        <span style="color:orange;">●</span>
        Moderate Risk<br>

        <span style="color:red;">●</span>
        High Risk
    </div>
    """

    m.get_root().html.add_child(
        folium.Element(legend_html)
    )

    folium.LayerControl().add_to(m)

    return m