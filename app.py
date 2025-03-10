import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from sklearn.ensemble import IsolationForest
import os

# OpenSky Network API'den uçuş verilerini çekme
URL = "https://opensky-network.org/api/states/all"
response = requests.get(URL)
data = response.json()

# API'den gelen veriyi direkt DataFrame'e çevirme
columns = ["icao24", "callsign", "origin_country", "time_position", "last_contact",
           "longitude", "latitude", "altitude", "on_ground", "velocity", "heading", "vertical_rate"]

# Eğer gelen veri beklenenden fazla sütun içeriyorsa, sadece ilk 12 sütunu al
flights = pd.DataFrame(data['states'])

# Sütunları ilk 12'ye düşürerek eşleştir
flights = flights.iloc[:, :len(columns)]
flights.columns = columns  # Sütun isimlerini ekle

# Eksik verileri temizle
flights.dropna(subset=['longitude', 'latitude', 'velocity'], inplace=True)

# Harita oluşturma
flight_map = folium.Map(location=[flights['latitude'].mean(), flights['longitude'].mean()], zoom_start=6)

# MarkerCluster kullanarak uçuşları gruplandırma
marker_cluster = MarkerCluster().add_to(flight_map)

# Uçuşların haritada görselleştirilmesi
for _, row in flights.iterrows():
    color = 'blue'  # Varsayılan renk
    
    # Popup içeriklerinin düzenlenmesi
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

# Anomali tespiti için Isolation Forest modeli
X = flights[['velocity', 'altitude', 'vertical_rate']]
anomaly_detector = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
flights['anomaly'] = anomaly_detector.fit_predict(X)

# Anormal uçuşları belirleme
anomalies = flights[flights['anomaly'] == -1]
print(f"Tespit edilen anormal uçuşlar: {len(anomalies)}")

# Anormal uçuşları haritada sadece bir kez gösterme
added_flights = set()  # Haritaya eklenen uçuşları saklamak için bir set
for _, row in anomalies.iterrows():
    # Eğer uçuş zaten eklenmişse, tekrar eklenmesin
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

# Haritayı "static" klasöründe kaydetme
if not os.path.exists('static'):
    os.makedirs('static')

flight_map.save('static/flight_radar_map_with_anomalies.html')

print("Harita kaydedildi: static/flight_radar_map_with_anomalies.html")
