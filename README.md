# IoT Sensor Dashboard

Een interactief dashboard voor het monitoren, visualiseren en analyseren van IoT-sensorgegevens.

## Functies

- Integratie met meerdere IoT-platformen:
  - AWS IoT Core
  - Azure IoT Hub
  - ThingSpeak
  - MQTT Broker
  - Custom API endpoints
- Real-time sensorgegevens visualisatie
- Historische gegevensanalyse
- Configureerbare waarschuwingen
- Ondersteuning voor verschillende sensortypes (temperatuur, luchtvochtigheid, druk, beweging, etc.)

## Vereisten

- Python 3.6+
- Streamlit
- Pandas
- Plotly
- PyYAML
- Paho-MQTT

## Installatie

```bash
# Clone de repository
git clone https://github.com/uw-gebruikersnaam/iot-sensor-dashboard.git
cd iot-sensor-dashboard

# Installeer afhankelijkheden
pip install -r requirements.txt
```

## Gebruik

```bash
streamlit run app.py
```

Open uw browser en ga naar http://localhost:8501 om het dashboard te bekijken.

## Configuratie

Het dashboard kan worden geconfigureerd met het `config.yaml`-bestand. Hier kunt u IoT-platformintegraties, sensortypes en waarschuwingsparameters aanpassen.

## Licentie

MIT