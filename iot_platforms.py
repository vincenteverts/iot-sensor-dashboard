import os
import requests
import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import random

class IoTPlatform:
    """Base class for IoT platform integrations"""
    
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.connected = False
    
    def test_connection(self):
        """Test connection to the platform"""
        raise NotImplementedError("Subclasses must implement test_connection()")
    
    def discover_sensors(self):
        """Discover available sensors"""
        raise NotImplementedError("Subclasses must implement discover_sensors()")
    
    def get_latest_data(self, sensor_id):
        """Get latest data for a sensor"""
        raise NotImplementedError("Subclasses must implement get_latest_data()")
    
    def get_historical_data(self, sensor_id, start_time, end_time):
        """Get historical data for a sensor within time range"""
        raise NotImplementedError("Subclasses must implement get_historical_data()")


class AWSIoTPlatform(IoTPlatform):
    """AWS IoT Core platform integration"""
    
    def __init__(self, connection_params):
        super().__init__(connection_params)
        self.endpoint = connection_params.get('endpoint', '')
        self.access_key = connection_params.get('access_key', '')
        self.secret_key = connection_params.get('secret_key', '')
        self.region = connection_params.get('region', 'us-east-1')
        
        # In a real implementation, we would initialize boto3 client here
        # self.client = boto3.client(
        #     'iot-data',
        #     region_name=self.region,
        #     aws_access_key_id=self.access_key,
        #     aws_secret_access_key=self.secret_key,
        #     endpoint_url=f'https://{self.endpoint}'
        # )
    
    def test_connection(self):
        """Test connection to AWS IoT Core"""
        try:
            # In a real implementation, we would make an actual API call
            # For now, just check if credentials are present
            if self.endpoint and self.access_key and self.secret_key:
                self.connected = True
                return True
            return False
        except Exception as e:
            print(f"Error connecting to AWS IoT: {str(e)}")
            return False
    
    def discover_sensors(self):
        """Discover available sensors from AWS IoT"""
        # In a real implementation, we would query AWS IoT for devices and their shadows
        # For demonstration, return some sample sensors
        if not self.connected:
            return []
        
        return [
            {
                'id': 'aws-temp-001',
                'name': 'AWS Temperature Sensor 1',
                'type': 'temperature',
                'location': 'Living Room',
                'metadata': {
                    'manufacturer': 'AWS',
                    'model': 'TempSensor',
                    'firmware': '1.2.3'
                }
            },
            {
                'id': 'aws-humid-001',
                'name': 'AWS Humidity Sensor 1',
                'type': 'humidity',
                'location': 'Living Room',
                'metadata': {
                    'manufacturer': 'AWS',
                    'model': 'HumidSensor',
                    'firmware': '1.1.0'
                }
            },
            {
                'id': 'aws-motion-001',
                'name': 'AWS Motion Sensor 1',
                'type': 'motion',
                'location': 'Entrance',
                'metadata': {
                    'manufacturer': 'AWS',
                    'model': 'MotionSensor',
                    'firmware': '2.0.1'
                }
            }
        ]
    
    def get_latest_data(self, sensor_id):
        """Get latest data for an AWS IoT sensor"""
        if not self.connected:
            raise Exception("Not connected to AWS IoT")
        
        # In a real implementation, we would query the device shadow
        # For demonstration, generate plausible data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if 'temp' in sensor_id:
            value = round(random.uniform(18.0, 26.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': '°C'
            }
        elif 'humid' in sensor_id:
            value = round(random.uniform(30.0, 70.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': '%'
            }
        elif 'motion' in sensor_id:
            value = random.choice([0, 1])
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': 'binary'
            }
        else:
            raise Exception(f"Unknown sensor type for ID: {sensor_id}")
    
    def get_historical_data(self, sensor_id, start_time, end_time):
        """Get historical data for an AWS IoT sensor"""
        if not self.connected:
            raise Exception("Not connected to AWS IoT")
        
        # In a real implementation, we would query AWS TimeStream or similar
        # For demonstration, generate plausible historical data
        data = []
        current_time = start_time
        
        while current_time <= end_time:
            if 'temp' in sensor_id:
                value = round(random.uniform(18.0, 26.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': '°C'
                })
            elif 'humid' in sensor_id:
                value = round(random.uniform(30.0, 70.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': '%'
                })
            elif 'motion' in sensor_id:
                value = random.choice([0, 1])
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': 'binary'
                })
            
            # Increment by a random number of minutes (1-5) to simulate irregular data
            current_time += timedelta(minutes=random.randint(1, 5))
        
        return data


class AzureIoTPlatform(IoTPlatform):
    """Azure IoT Hub platform integration"""
    
    def __init__(self, connection_params):
        super().__init__(connection_params)
        self.connection_string = connection_params.get('connection_string', '')
        self.hub_name = connection_params.get('hub_name', '')
        
        # In a real implementation, we would initialize the Azure SDK client
    
    def test_connection(self):
        """Test connection to Azure IoT Hub"""
        try:
            # In a real implementation, we would make an actual API call
            # For now, just check if connection string is present
            if self.connection_string:
                self.connected = True
                return True
            return False
        except Exception as e:
            print(f"Error connecting to Azure IoT Hub: {str(e)}")
            return False
    
    def discover_sensors(self):
        """Discover available sensors from Azure IoT Hub"""
        if not self.connected:
            return []
        
        # Sample sensors for demonstration
        return [
            {
                'id': 'azure-temp-001',
                'name': 'Azure Temperature Sensor 1',
                'type': 'temperature',
                'location': 'Kitchen',
                'metadata': {
                    'manufacturer': 'Microsoft',
                    'model': 'AzureTempSensor',
                    'firmware': '2.1.3'
                }
            },
            {
                'id': 'azure-pressure-001',
                'name': 'Azure Pressure Sensor 1',
                'type': 'pressure',
                'location': 'Outdoor',
                'metadata': {
                    'manufacturer': 'Microsoft',
                    'model': 'AzurePressureSensor',
                    'firmware': '1.0.5'
                }
            },
            {
                'id': 'azure-light-001',
                'name': 'Azure Light Sensor 1',
                'type': 'light',
                'location': 'Living Room',
                'metadata': {
                    'manufacturer': 'Microsoft',
                    'model': 'AzureLightSensor',
                    'firmware': '1.2.0'
                }
            }
        ]
    
    def get_latest_data(self, sensor_id):
        """Get latest data for an Azure IoT sensor"""
        if not self.connected:
            raise Exception("Not connected to Azure IoT Hub")
        
        # Generate plausible data for demonstration
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if 'temp' in sensor_id:
            value = round(random.uniform(18.0, 26.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': '°C'
            }
        elif 'pressure' in sensor_id:
            value = round(random.uniform(980.0, 1020.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': 'hPa'
            }
        elif 'light' in sensor_id:
            value = round(random.uniform(0, 1000), 0)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': 'lux'
            }
        else:
            raise Exception(f"Unknown sensor type for ID: {sensor_id}")
    
    def get_historical_data(self, sensor_id, start_time, end_time):
        """Get historical data for an Azure IoT sensor"""
        if not self.connected:
            raise Exception("Not connected to Azure IoT Hub")
        
        # Generate plausible historical data
        data = []
        current_time = start_time
        
        while current_time <= end_time:
            if 'temp' in sensor_id:
                # Simulate a temperature pattern through the day
                hour = current_time.hour
                base_temp = 20.0 + (hour - 12) * 0.5 if hour > 12 else 20.0 - (12 - hour) * 0.2
                value = round(base_temp + random.uniform(-1.0, 1.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': '°C'
                })
            elif 'pressure' in sensor_id:
                value = round(random.uniform(980.0, 1020.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': 'hPa'
                })
            elif 'light' in sensor_id:
                # Simulate day/night cycle
                hour = current_time.hour
                if 6 <= hour <= 18:  # Daytime
                    value = round(random.uniform(300, 1000), 0)
                else:  # Nighttime
                    value = round(random.uniform(0, 50), 0)
                
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': 'lux'
                })
            
            current_time += timedelta(minutes=random.randint(1, 5))
        
        return data


class ThingSpeakPlatform(IoTPlatform):
    """ThingSpeak IoT platform integration"""
    
    def __init__(self, connection_params):
        super().__init__(connection_params)
        self.api_key = connection_params.get('api_key', '')
        self.channel_id = connection_params.get('channel_id', '')
        self.base_url = "https://api.thingspeak.com"
    
    def test_connection(self):
        """Test connection to ThingSpeak"""
        try:
            # For a real implementation, we would make an API call to ThingSpeak
            if self.api_key and self.channel_id:
                # For demo, simulate a successful connection
                self.connected = True
                return True
            return False
        except Exception as e:
            print(f"Error connecting to ThingSpeak: {str(e)}")
            return False
    
    def discover_sensors(self):
        """Discover available sensors from ThingSpeak channel"""
        if not self.connected:
            return []
        
        # In a real implementation, we would query the channel feed to determine available fields
        # For demonstration, return sample sensors
        return [
            {
                'id': f'ts-temp-{self.channel_id}',
                'name': 'ThingSpeak Temperature Sensor',
                'type': 'temperature',
                'location': 'Bedroom',
                'metadata': {
                    'channel_id': self.channel_id,
                    'field': 'field1'
                }
            },
            {
                'id': f'ts-humid-{self.channel_id}',
                'name': 'ThingSpeak Humidity Sensor',
                'type': 'humidity',
                'location': 'Bedroom',
                'metadata': {
                    'channel_id': self.channel_id,
                    'field': 'field2'
                }
            }
        ]
    
    def get_latest_data(self, sensor_id):
        """Get latest data for a ThingSpeak sensor"""
        if not self.connected:
            raise Exception("Not connected to ThingSpeak")
        
        # For demonstration, generate plausible data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if 'temp' in sensor_id:
            value = round(random.uniform(18.0, 26.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': '°C'
            }
        elif 'humid' in sensor_id:
            value = round(random.uniform(30.0, 70.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': '%'
            }
        else:
            raise Exception(f"Unknown sensor type for ID: {sensor_id}")
    
    def get_historical_data(self, sensor_id, start_time, end_time):
        """Get historical data for a ThingSpeak sensor"""
        if not self.connected:
            raise Exception("Not connected to ThingSpeak")
        
        # Generate plausible historical data
        data = []
        current_time = start_time
        
        while current_time <= end_time:
            if 'temp' in sensor_id:
                value = round(random.uniform(18.0, 26.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': '°C'
                })
            elif 'humid' in sensor_id:
                value = round(random.uniform(30.0, 70.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': '%'
                })
            
            current_time += timedelta(minutes=random.randint(5, 10))
        
        return data


class MQTTPlatform(IoTPlatform):
    """MQTT broker platform integration"""
    
    def __init__(self, connection_params):
        super().__init__(connection_params)
        self.broker = connection_params.get('broker', 'localhost')
        self.port = int(connection_params.get('port', 1883))
        self.username = connection_params.get('username', '')
        self.password = connection_params.get('password', '')
        self.client_id = f"iot-dashboard-{int(time.time())}"
        self.topics = connection_params.get('topics', 'sensors/#').split(',')
        self.client = None
        self.messages = {}
    
    def test_connection(self):
        """Test connection to MQTT broker"""
        try:
            # Create MQTT client
            self.client = mqtt.Client(client_id=self.client_id)
            
            # Set credentials if provided
            if self.username and self.password:
                self.client.username_pw_set(self.username, self.password)
            
            # Set callbacks
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            
            # Connect with a short timeout
            self.client.connect(self.broker, self.port, 10)
            self.client.loop_start()
            
            # Wait a moment for connection to establish
            time.sleep(2)
            
            if self.connected:
                return True
            else:
                self.client.loop_stop()
                return False
        except Exception as e:
            print(f"Error connecting to MQTT broker: {str(e)}")
            if self.client:
                self.client.loop_stop()
            return False
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback when MQTT client connects"""
        if rc == 0:
            self.connected = True
            # Subscribe to topics
            for topic in self.topics:
                client.subscribe(topic.strip())
        else:
            self.connected = False
    
    def _on_message(self, client, userdata, msg):
        """Callback when MQTT client receives a message"""
        try:
            # Store received message
            self.messages[msg.topic] = {
                'payload': msg.payload.decode('utf-8'),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error processing MQTT message: {str(e)}")
    
    def discover_sensors(self):
        """Discover available sensors from MQTT topics"""
        if not self.connected:
            return []
        
        # For a real implementation, we would analyze MQTT topics and messages
        # For demonstration, return some sample sensors based on topics
        sensors = []
        
        # Add some sample sensors based on topics
        for i, topic in enumerate(self.topics):
            topic_parts = topic.split('/')
            base_name = topic_parts[-1] if len(topic_parts) > 1 else f"sensor{i+1}"
            
            # Create temperature sensor
            sensors.append({
                'id': f'mqtt-temp-{i+1}',
                'name': f'MQTT Temperature {base_name}',
                'type': 'temperature',
                'location': 'MQTT Network',
                'metadata': {
                    'topic': f"{topic}/temperature"
                }
            })
            
            # Create humidity sensor
            sensors.append({
                'id': f'mqtt-humid-{i+1}',
                'name': f'MQTT Humidity {base_name}',
                'type': 'humidity',
                'location': 'MQTT Network',
                'metadata': {
                    'topic': f"{topic}/humidity"
                }
            })
        
        return sensors
    
    def get_latest_data(self, sensor_id):
        """Get latest data for an MQTT sensor"""
        if not self.connected:
            raise Exception("Not connected to MQTT broker")
        
        # For a real implementation, we would look up the latest message for this sensor's topic
        # For demonstration, generate plausible data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if 'temp' in sensor_id:
            value = round(random.uniform(18.0, 26.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': '°C'
            }
        elif 'humid' in sensor_id:
            value = round(random.uniform(30.0, 70.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': '%'
            }
        else:
            raise Exception(f"Unknown sensor type for ID: {sensor_id}")
    
    def get_historical_data(self, sensor_id, start_time, end_time):
        """Get historical data for an MQTT sensor"""
        if not self.connected:
            raise Exception("Not connected to MQTT broker")
        
        # MQTT doesn't natively store historical data, would typically be saved elsewhere
        # For demonstration, generate plausible historical data
        data = []
        current_time = start_time
        
        while current_time <= end_time:
            if 'temp' in sensor_id:
                value = round(random.uniform(18.0, 26.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': '°C'
                })
            elif 'humid' in sensor_id:
                value = round(random.uniform(30.0, 70.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': '%'
                })
            
            current_time += timedelta(minutes=random.randint(1, 3))
        
        return data
    
    def __del__(self):
        """Clean up MQTT client connection on deletion"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()


class CustomAPIPlatform(IoTPlatform):
    """Custom REST API platform integration"""
    
    def __init__(self, connection_params):
        super().__init__(connection_params)
        self.base_url = connection_params.get('base_url', '')
        self.api_key = connection_params.get('api_key', '')
        self.username = connection_params.get('username', '')
        self.password = connection_params.get('password', '')
    
    def test_connection(self):
        """Test connection to Custom API"""
        try:
            # For a real implementation, we would make an API call to the endpoint
            # For now, simulate connection success if the base_url is provided
            if self.base_url:
                self.connected = True
                return True
            return False
        except Exception as e:
            print(f"Error connecting to Custom API: {str(e)}")
            return False
    
    def discover_sensors(self):
        """Discover available sensors from Custom API"""
        if not self.connected:
            return []
        
        # For demonstration, return sample sensors
        return [
            {
                'id': 'api-temp-001',
                'name': 'API Temperature Sensor 1',
                'type': 'temperature',
                'location': 'Office',
                'metadata': {
                    'endpoint': f"{self.base_url}/sensors/temperature/1"
                }
            },
            {
                'id': 'api-co2-001',
                'name': 'API CO2 Sensor 1',
                'type': 'co2',
                'location': 'Office',
                'metadata': {
                    'endpoint': f"{self.base_url}/sensors/co2/1"
                }
            },
            {
                'id': 'api-occupancy-001',
                'name': 'API Occupancy Sensor 1',
                'type': 'occupancy',
                'location': 'Conference Room',
                'metadata': {
                    'endpoint': f"{self.base_url}/sensors/occupancy/1"
                }
            }
        ]
    
    def get_latest_data(self, sensor_id):
        """Get latest data for a Custom API sensor"""
        if not self.connected:
            raise Exception("Not connected to Custom API")
        
        # For demonstration, generate plausible data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if 'temp' in sensor_id:
            value = round(random.uniform(18.0, 26.0), 1)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': '°C'
            }
        elif 'co2' in sensor_id:
            value = round(random.uniform(400.0, 1200.0), 0)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': 'ppm'
            }
        elif 'occupancy' in sensor_id:
            value = random.randint(0, 10)
            return {
                'sensor_id': sensor_id,
                'timestamp': timestamp,
                'value': value,
                'unit': 'people'
            }
        else:
            raise Exception(f"Unknown sensor type for ID: {sensor_id}")
    
    def get_historical_data(self, sensor_id, start_time, end_time):
        """Get historical data for a Custom API sensor"""
        if not self.connected:
            raise Exception("Not connected to Custom API")
        
        # Generate plausible historical data
        data = []
        current_time = start_time
        
        while current_time <= end_time:
            if 'temp' in sensor_id:
                value = round(random.uniform(18.0, 26.0), 1)
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': '°C'
                })
            elif 'co2' in sensor_id:
                # Simulate CO2 levels with higher values during work hours
                hour = current_time.hour
                if 8 <= hour <= 18:  # Working hours
                    value = round(random.uniform(600.0, 1200.0), 0)
                else:  # Off hours
                    value = round(random.uniform(400.0, 600.0), 0)
                
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': 'ppm'
                })
            elif 'occupancy' in sensor_id:
                # Simulate occupancy with higher values during work hours
                hour = current_time.hour
                weekday = current_time.weekday()
                
                if weekday < 5 and 8 <= hour <= 18:  # Weekday working hours
                    value = random.randint(1, 10)
                else:  # Weekend or off hours
                    value = random.randint(0, 2)
                
                data.append({
                    'sensor_id': sensor_id,
                    'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'unit': 'people'
                })
            
            current_time += timedelta(minutes=random.randint(5, 15))
        
        return data


class IoTPlatformFactory:
    """Factory class to create IoT platform instances"""
    
    def create_platform(self, platform_type, connection_params):
        """Create and return an instance of the specified platform type"""
        if platform_type == 'AWS IoT Core':
            return AWSIoTPlatform(connection_params)
        elif platform_type == 'Azure IoT Hub':
            return AzureIoTPlatform(connection_params)
        elif platform_type == 'ThingSpeak':
            return ThingSpeakPlatform(connection_params)
        elif platform_type == 'MQTT Broker':
            return MQTTPlatform(connection_params)
        elif platform_type == 'Custom API':
            return CustomAPIPlatform(connection_params)
        else:
            raise ValueError(f"Unsupported platform type: {platform_type}")
