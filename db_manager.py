import pandas as pd
from datetime import datetime
import sqlite3
import os
import json

class DatabaseManager:
    """Manage sensor data storage and retrieval"""
    
    def __init__(self, db_path=None):
        """Initialize the database manager"""
        # For simplicity, we'll use an in-memory database
        # In a production environment, you'd want to use a proper database
        self.data = {}  # Dictionary to store sensor data by sensor_id
    
    def insert_sensor_data(self, data):
        """Insert sensor data into the database"""
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        
        required_fields = ['sensor_id', 'timestamp', 'value']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Data missing required field: {field}")
        
        sensor_id = data['sensor_id']
        
        # Create entry for this sensor if it doesn't exist
        if sensor_id not in self.data:
            self.data[sensor_id] = []
        
        # Add the data point
        self.data[sensor_id].append(data.copy())
        
        return True
    
    def query_sensor_data(self, sensor_id, start_time, end_time):
        """Query sensor data for a specific time range"""
        if sensor_id not in self.data:
            return []
        
        # Filter data by time range
        result = []
        for item in self.data[sensor_id]:
            item_time = item['timestamp']
            if isinstance(item_time, str):
                item_time = datetime.strptime(item_time, "%Y-%m-%d %H:%M:%S")
            
            if start_time <= item_time <= end_time:
                result.append(item.copy())
        
        return result
    
    def query_latest_sensor_data(self, sensor_id):
        """Query the latest data point for a sensor"""
        if sensor_id not in self.data or not self.data[sensor_id]:
            return None
        
        # Get the latest item (assuming data is appended chronologically)
        latest = self.data[sensor_id][-1].copy()
        
        return latest
    
    def delete_sensor_data(self, sensor_id=None, older_than=None):
        """Delete sensor data, optionally filtering by sensor_id and age"""
        if sensor_id and sensor_id in self.data:
            if older_than:
                # Delete only data older than the specified date
                cutoff_time = older_than
                if isinstance(cutoff_time, str):
                    cutoff_time = datetime.strptime(cutoff_time, "%Y-%m-%d %H:%M:%S")
                
                self.data[sensor_id] = [
                    item for item in self.data[sensor_id]
                    if datetime.strptime(item['timestamp'], "%Y-%m-%d %H:%M:%S") >= cutoff_time
                ]
            else:
                # Delete all data for this sensor
                self.data[sensor_id] = []
            return True
        elif sensor_id is None and older_than:
            # Delete data older than the specified date for all sensors
            cutoff_time = older_than
            if isinstance(cutoff_time, str):
                cutoff_time = datetime.strptime(cutoff_time, "%Y-%m-%d %H:%M:%S")
            
            for sid in self.data:
                self.data[sid] = [
                    item for item in self.data[sid]
                    if datetime.strptime(item['timestamp'], "%Y-%m-%d %H:%M:%S") >= cutoff_time
                ]
            return True
        elif sensor_id is None:
            # Clear all data
            self.data = {}
            return True
        
        return False
    
    def get_sensors_with_data(self):
        """Get a list of sensor IDs that have data"""
        return list(self.data.keys())
    
    def export_to_csv(self, sensor_id, filepath):
        """Export sensor data to a CSV file"""
        if sensor_id not in self.data or not self.data[sensor_id]:
            return False
        
        # Convert to DataFrame
        df = pd.DataFrame(self.data[sensor_id])
        
        # Export to CSV
        df.to_csv(filepath, index=False)
        
        return True
    
    def import_from_csv(self, sensor_id, filepath):
        """Import sensor data from a CSV file"""
        if not os.path.exists(filepath):
            return False
        
        # Read CSV file
        df = pd.read_csv(filepath)
        
        # Convert to list of dictionaries
        data_list = df.to_dict('records')
        
        # Add each data point
        for data in data_list:
            data['sensor_id'] = sensor_id
            self.insert_sensor_data(data)
        
        return True
