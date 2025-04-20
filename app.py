import os
import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from sklearn.ensemble import IsolationForest
from flask import Flask, render_template

# Flask uygulamasını başlat
app = Flask(__name__)

# Uçuş verilerini çeken ve haritayı üreten fonksiyon
def generate_flight_map():
    # OpenSky Network API'den uçuş verilerini çekme
    URL = "https://opensky-network.org/api/states/all"
    response = requests.get(URL)
    data = response.json()

    # API'den gelen veriyi direkt DataFrame'e çevirme
    columns = ["icao24", "callsign", "origin_country", "time_position", "last_contact",
               "longitude", "latitude", "altitude", "on_ground", "velocity", "heading", "vertical_rate"]

    # Eğer gelen veri beklenenden fazla sütun içeriyorsa, sadece ilk 12 sütunu al
    flights = pd.DataFrame(data['states'])
    flights = flights.iloc[:, :len(columns)]
    flights.columns = columns

    # Eksik verileri temizle
    flights.dropna(subset=['longitude', 'latitude', 'velocity'], inplace=True)

    # Harita oluşturma
    flight_map = folium.Map(location=[flights['latitude'].mean(), flights['longitude'].mean()], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(flight_map)

    # Uçuşların haritada görselleştirilmesi
    for _, row in flights.iterrows():
        color = 'blue'

        popup_content = f"""
        <div style="width: 300px; height: auto;">
            <b>Callsign:</b> {row['callsign']}<br>
            <b>Origin Country:</b> {row['origin_country']}<br>
            <b>Altitude:</b> {row['altitude']} meters<br>
            <b>Velocity:</b> {row['velocity']} m/s<br>
        </div>
        """

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)

    # Anomali tespiti
    X = flights[['velocity', 'altitude', 'vertical_rate']]
    anomaly_detector = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    flights['anomaly'] = anomaly_detector.fit_predict(X)

    anomalies = flights[flights['anomaly'] == -1]

    added_flights = set()
    for _, row in anomalies.iterrows():
        if row['icao24'] not in added_flights:
            added_flights.add(row['icao24'])

            popup_content = f"""
            <div style="width: 300px; height: auto;">
                <b>Callsign:</b> {row['callsign']}<br>
                <b>Origin Country:</b> {row['origin_country']}<br>
                <b>Altitude:</b> {row['altitude']} meters<br>
                <b>Velocity:</b> {row['velocity']} m/s<br>
                <b>Anomaly Detected!</b>
            </div>
            """

            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color='red')
            ).add_to(marker_cluster)

    # static klasörü oluştur ve haritayı kaydet
    if not os.path.exists('static'):
        os.makedirs('static')

    flight_map.save('static/flight_radar_map_with_anomalies.html')

# Ana sayfa route'u
@app.route('/')
def index():
    generate_flight_map()
    return render_template('index.html')

# Flask server'ı başlat
if __name__ == '__main__':
    app.run(debug=True)
