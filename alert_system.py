import streamlit as st
from datetime import datetime

class AlertSystem:
    """System for defining and checking sensor alerts"""
    
    def __init__(self):
        """Initialize the alert system"""
        # Alert configs stored as a list of dictionaries with sensor_id, type, threshold, etc.
        self.alert_configs = []
    
    def add_alert_config(self, config):
        """Add a new alert configuration"""
        if not isinstance(config, dict):
            raise ValueError("Alert configuration must be a dictionary")
        
        required_fields = ['sensor_id', 'type', 'threshold']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Alert config missing required field: {field}")
        
        # Add the alert config
        self.alert_configs.append(config)
        return True
    
    def remove_alert_config(self, index):
        """Remove an alert configuration by index"""
        if 0 <= index < len(self.alert_configs):
            del self.alert_configs[index]
            return True
        return False
    
    def get_alert_configs(self):
        """Get all alert configurations"""
        return self.alert_configs
    
    def check_alerts(self, sensor, data):
        """Check data against alert configurations and return triggered alerts"""
        if not isinstance(data, dict) or 'value' not in data:
            return []
        
        triggered_alerts = []
        
        # Find alert configs for this sensor
        for config in self.alert_configs:
            if config['sensor_id'] == sensor['id']:
                alert_type = config['type']
                threshold = config['threshold']
                
                # Check different alert types
                if alert_type == 'Threshold High' and data['value'] > threshold:
                    triggered_alerts.append(
                        f"{sensor['name']} value {data['value']} exceeds threshold {threshold}"
                    )
                elif alert_type == 'Threshold Low' and data['value'] < threshold:
                    triggered_alerts.append(
                        f"{sensor['name']} value {data['value']} is below threshold {threshold}"
                    )
                elif alert_type == 'Change Rate':
                    # For change rate alerts, we need previous data
                    # This is a simplified implementation
                    pass
        
        return triggered_alerts
    
    def _get_prev_value(self, sensor_id, db_manager):
        """Get the previous value for a sensor to calculate change rate"""
        # Query the latest two values for this sensor and calculate the change rate
        # This is a placeholder - in a real implementation, we would query the database
        pass

class AlertNotifier:
    """Send notifications for triggered alerts"""
    
    def __init__(self, config=None):
        """Initialize with notification configuration"""
        self.config = config or {}
    
    def send_email_notification(self, alert_message):
        """Send an email notification for an alert"""
        # In a real implementation, this would connect to an email service
        # For demonstration, just log the notification
        print(f"[EMAIL NOTIFICATION] {datetime.now()}: {alert_message}")
        return True
    
    def send_sms_notification(self, alert_message):
        """Send an SMS notification for an alert"""
        # In a real implementation, this would connect to an SMS service
        # For demonstration, just log the notification
        print(f"[SMS NOTIFICATION] {datetime.now()}: {alert_message}")
        return True
    
    def send_webhook_notification(self, alert_data):
        """Send a webhook notification for an alert"""
        # In a real implementation, this would make an HTTP request to a webhook endpoint
        # For demonstration, just log the notification
        print(f"[WEBHOOK NOTIFICATION] {datetime.now()}: {alert_data}")
        return True
    
    def send_notification(self, alert, notification_type='email'):
        """Send a notification of the specified type"""
        if notification_type == 'email':
            return self.send_email_notification(alert)
        elif notification_type == 'sms':
            return self.send_sms_notification(alert)
        elif notification_type == 'webhook':
            return self.send_webhook_notification(alert)
        else:
            raise ValueError(f"Unsupported notification type: {notification_type}")
