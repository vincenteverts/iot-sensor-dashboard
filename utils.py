import yaml
import os
import random
from datetime import datetime, timedelta
import pandas as pd

def load_config(config_file='config.yaml'):
    """Load configuration from YAML file"""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    else:
        # Default configuration
        config = get_default_config()
        # Save default config
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
    
    return config

def get_default_config():
    """Get default configuration"""
    return {
        'app': {
            'name': 'IoT Sensor Dashboard',
            'version': '1.0.0',
            'refresh_interval': 5,  # seconds
            'max_history_days': 30
        },
        'platforms': {
            'AWS IoT Core': {
                'description': 'Amazon Web Services IoT Core platform',
                'connection_params': {
                    'endpoint': {
                        'label': 'AWS IoT Endpoint',
                        'default': '',
                        'env_var': 'AWS_IOT_ENDPOINT'
                    },
                    'region': {
                        'label': 'AWS Region',
                        'default': 'us-east-1',
                        'env_var': 'AWS_REGION'
                    },
                    'access_key': {
                        'label': 'AWS Access Key ID',
                        'default': '',
                        'env_var': 'AWS_ACCESS_KEY_ID',
                        'sensitive': True
                    },
                    'secret_key': {
                        'label': 'AWS Secret Access Key',
                        'default': '',
                        'env_var': 'AWS_SECRET_ACCESS_KEY',
                        'sensitive': True
                    }
                }
            },
            'Azure IoT Hub': {
                'description': 'Microsoft Azure IoT Hub',
                'connection_params': {
                    'connection_string': {
                        'label': 'Connection String',
                        'default': '',
                        'env_var': 'AZURE_IOT_CONNECTION_STRING',
                        'sensitive': True
                    },
                    'hub_name': {
                        'label': 'IoT Hub Name',
                        'default': '',
                        'env_var': 'AZURE_IOT_HUB_NAME'
                    }
                }
            },
            'ThingSpeak': {
                'description': 'ThingSpeak IoT platform',
                'connection_params': {
                    'api_key': {
                        'label': 'API Key',
                        'default': '',
                        'env_var': 'THINGSPEAK_API_KEY',
                        'sensitive': True
                    },
                    'channel_id': {
                        'label': 'Channel ID',
                        'default': '',
                        'env_var': 'THINGSPEAK_CHANNEL_ID'
                    }
                }
            },
            'MQTT Broker': {
                'description': 'Generic MQTT broker',
                'connection_params': {
                    'broker': {
                        'label': 'Broker Address',
                        'default': 'mqtt.eclipse.org',
                        'env_var': 'MQTT_BROKER'
                    },
                    'port': {
                        'label': 'Port',
                        'default': '1883',
                        'env_var': 'MQTT_PORT'
                    },
                    'username': {
                        'label': 'Username (optional)',
                        'default': '',
                        'env_var': 'MQTT_USERNAME'
                    },
                    'password': {
                        'label': 'Password (optional)',
                        'default': '',
                        'env_var': 'MQTT_PASSWORD',
                        'sensitive': True
                    },
                    'topics': {
                        'label': 'Topics (comma-separated)',
                        'default': 'sensors/#',
                        'env_var': 'MQTT_TOPICS'
                    }
                }
            },
            'Custom API': {
                'description': 'Custom REST API endpoint',
                'connection_params': {
                    'base_url': {
                        'label': 'Base URL',
                        'default': 'https://api.example.com',
                        'env_var': 'API_BASE_URL'
                    },
                    'api_key': {
                        'label': 'API Key (optional)',
                        'default': '',
                        'env_var': 'API_KEY',
                        'sensitive': True
                    },
                    'username': {
                        'label': 'Username (optional)',
                        'default': '',
                        'env_var': 'API_USERNAME'
                    },
                    'password': {
                        'label': 'Password (optional)',
                        'default': '',
                        'env_var': 'API_PASSWORD',
                        'sensitive': True
                    }
                }
            }
        },
        'sensor_types': {
            'temperature': {
                'name': 'Temperature',
                'unit': '°C',
                'icon': 'thermometer',
                'min': -50,
                'max': 150
            },
            'humidity': {
                'name': 'Humidity',
                'unit': '%',
                'icon': 'droplet',
                'min': 0,
                'max': 100
            },
            'pressure': {
                'name': 'Pressure',
                'unit': 'hPa',
                'icon': 'activity',
                'min': 900,
                'max': 1100
            },
            'co2': {
                'name': 'CO2',
                'unit': 'ppm',
                'icon': 'wind',
                'min': 0,
                'max': 5000
            },
            'light': {
                'name': 'Light',
                'unit': 'lux',
                'icon': 'sun',
                'min': 0,
                'max': 10000
            },
            'motion': {
                'name': 'Motion',
                'unit': 'binary',
                'icon': 'activity',
                'min': 0,
                'max': 1
            },
            'occupancy': {
                'name': 'Occupancy',
                'unit': 'count',
                'icon': 'users',
                'min': 0,
                'max': 100
            }
        },
        'alerts': {
            'email': {
                'enabled': False,
                'smtp_server': '',
                'smtp_port': 587,
                'username': '',
                'password': '',
                'from_addr': '',
                'to_addrs': []
            },
            'sms': {
                'enabled': False,
                'provider': '',
                'api_key': '',
                'phone_numbers': []
            }
        }
    }

def get_demo_data(sensor_type, num_points=100):
    """Generate demo data for a sensor type"""
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    data = []
    
    # Generate data points at regular intervals
    time_delta = (end_time - start_time) / num_points
    current_time = start_time
    
    for i in range(num_points):
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if sensor_type == 'temperature':
            # Simulate temperature variations through the day
            hour = current_time.hour
            base_temp = 20.0
            if hour < 6:  # Night
                base_temp = 18.0 + random.uniform(-1, 1)
            elif hour < 12:  # Morning
                base_temp = 19.0 + (hour - 6) * 0.5 + random.uniform(-0.5, 0.5)
            elif hour < 18:  # Afternoon
                base_temp = 22.0 + random.uniform(-0.5, 0.5)
            else:  # Evening
                base_temp = 22.0 - (hour - 18) * 0.5 + random.uniform(-0.5, 0.5)
            
            value = round(base_temp, 1)
            unit = '°C'
        
        elif sensor_type == 'humidity':
            # Simulate humidity variations
            hour = current_time.hour
            if hour < 6:  # Night
                value = round(random.uniform(40, 50), 1)
            elif hour < 12:  # Morning
                value = round(random.uniform(45, 60), 1)
            elif hour < 18:  # Afternoon
                value = round(random.uniform(30, 50), 1)
            else:  # Evening
                value = round(random.uniform(40, 55), 1)
            
            unit = '%'
        
        elif sensor_type == 'pressure':
            # Simulate atmospheric pressure
            base_pressure = 1013.0
            daily_variation = 5.0 * math.sin(2 * math.pi * i / num_points)
            random_variation = random.uniform(-2, 2)
            value = round(base_pressure + daily_variation + random_variation, 1)
            unit = 'hPa'
        
        elif sensor_type == 'co2':
            # Simulate CO2 levels
            hour = current_time.hour
            if 8 <= hour <= 18:  # Working hours
                value = round(random.uniform(600, 1200), 0)
            else:  # Off hours
                value = round(random.uniform(400, 600), 0)
            
            unit = 'ppm'
        
        elif sensor_type == 'light':
            # Simulate light levels based on time of day
            hour = current_time.hour
            if hour < 6 or hour >= 20:  # Night
                value = round(random.uniform(0, 10), 0)
            elif 6 <= hour < 8 or 18 <= hour < 20:  # Dawn/Dusk
                value = round(random.uniform(50, 200), 0)
            else:  # Daytime
                value = round(random.uniform(300, 1000), 0)
            
            unit = 'lux'
        
        elif sensor_type == 'motion':
            # Simulate motion detection
            hour = current_time.hour
            weekday = current_time.weekday()
            
            if weekday < 5 and 8 <= hour <= 18:  # Weekday working hours
                value = random.choice([0, 1, 1, 1])  # More likely to have motion
            else:  # Weekend or off hours
                value = random.choice([0, 0, 0, 1])  # Less likely to have motion
            
            unit = 'binary'
        
        elif sensor_type == 'occupancy':
            # Simulate occupancy
            hour = current_time.hour
            weekday = current_time.weekday()
            
            if weekday < 5:  # Weekday
                if 8 <= hour < 9:  # Arrival time
                    value = random.randint(1, 10)
                elif 9 <= hour < 12:  # Morning work
                    value = random.randint(5, 15)
                elif 12 <= hour < 13:  # Lunch
                    value = random.randint(2, 8)
                elif 13 <= hour < 17:  # Afternoon work
                    value = random.randint(5, 15)
                elif 17 <= hour < 18:  # Departure time
                    value = random.randint(1, 5)
                else:  # Off hours
                    value = random.randint(0, 2)
            else:  # Weekend
                value = random.randint(0, 2)
            
            unit = 'count'
        
        else:
            # Default random value
            value = round(random.uniform(0, 100), 1)
            unit = 'value'
        
        data.append({
            'timestamp': timestamp,
            'value': value,
            'unit': unit
        })
        
        current_time += time_delta
    
    return data

import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates in kilometers"""
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert coordinates from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Difference in coordinates
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance

def format_value(value, sensor_type, precision=1):
    """Format a sensor value based on its type"""
    if sensor_type in ['temperature', 'humidity', 'pressure']:
        return f"{value:.{precision}f}"
    elif sensor_type in ['co2', 'light', 'occupancy']:
        return f"{int(value)}"
    elif sensor_type == 'motion':
        return "Active" if value else "Inactive"
    else:
        return str(value)

def get_sensor_icon(sensor_type):
    """Get an icon name for a sensor type"""
    icons = {
        'temperature': 'thermometer',
        'humidity': 'droplet',
        'pressure': 'activity',
        'co2': 'wind',
        'light': 'sun',
        'motion': 'activity',
        'occupancy': 'users',
        'default': 'box'
    }
    return icons.get(sensor_type, icons['default'])
