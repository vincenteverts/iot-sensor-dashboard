import pandas as pd
from datetime import datetime
import json
import os

class DataHandler:
    """Class to handle data processing and storage"""
    
    def __init__(self, db_manager):
        """Initialize with a database manager"""
        self.db_manager = db_manager
    
    def save_sensor_data(self, sensor_id, data):
        """Save sensor data to the database"""
        # Ensure data has the right format
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        
        required_fields = ['sensor_id', 'timestamp', 'value']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Data missing required field: {field}")
        
        # Save to database
        self.db_manager.insert_sensor_data(data)
        
        return True
    
    def get_sensor_data(self, sensor_id, start_time, end_time):
        """Retrieve sensor data from the database for a given time range"""
        return self.db_manager.query_sensor_data(sensor_id, start_time, end_time)
    
    def get_latest_sensor_data(self, sensor_id):
        """Get the most recent data point for a sensor"""
        return self.db_manager.query_latest_sensor_data(sensor_id)
    
    def calculate_statistics(self, data):
        """Calculate statistical metrics from sensor data"""
        if not data:
            return {
                'min': None,
                'max': None,
                'avg': None,
                'median': None,
                'std_dev': None
            }
        
        # Convert to DataFrame for easier analysis
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        
        # Calculate statistics
        stats = {
            'min': df['value'].min(),
            'max': df['value'].max(),
            'avg': df['value'].mean(),
            'median': df['value'].median(),
            'std_dev': df['value'].std()
        }
        
        return stats
    
    def detect_anomalies(self, data, threshold=2.0):
        """Detect anomalies in sensor data using simple statistical approach"""
        if not data or len(data) < 5:  # Need enough data points
            return []
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        
        # Calculate mean and standard deviation
        mean = df['value'].mean()
        std_dev = df['value'].std()
        
        # Find anomalies (values that are more than threshold standard deviations from the mean)
        anomalies = df[abs(df['value'] - mean) > threshold * std_dev]
        
        return anomalies.to_dict('records')
    
    def export_data(self, data, format='csv', filename=None):
        """Export sensor data to a file"""
        if not data:
            return False
        
        # Convert to DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sensor_data_{timestamp}.{format}"
        
        # Export based on format
        if format.lower() == 'csv':
            df.to_csv(filename, index=False)
        elif format.lower() == 'json':
            df.to_json(filename, orient='records')
        elif format.lower() == 'excel':
            df.to_excel(filename, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        return filename
