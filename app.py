import streamlit as st
import pandas as pd
import time
import yaml
import os
from datetime import datetime, timedelta

from iot_platforms import IoTPlatformFactory
from data_handlers import DataHandler
from visualization import create_line_chart, create_gauge_chart, create_bar_chart, create_stats_summary
from alert_system import AlertSystem
from db_manager import DatabaseManager
from utils import load_config, get_demo_data

# Page configuration
st.set_page_config(
    page_title="IoT Sensor Dashboard",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load configuration
config = load_config()

# Initialize session state variables if they don't exist
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'platform' not in st.session_state:
    st.session_state.platform = None
if 'sensors' not in st.session_state:
    st.session_state.sensors = []
if 'selected_sensors' not in st.session_state:
    st.session_state.selected_sensors = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager()
if 'data_handler' not in st.session_state:
    st.session_state.data_handler = DataHandler(st.session_state.db_manager)
if 'alert_system' not in st.session_state:
    st.session_state.alert_system = AlertSystem()

# Sidebar for platform selection and connection
st.sidebar.title("IoT Platform Connection")

platform_options = list(config['platforms'].keys())
selected_platform = st.sidebar.selectbox("Select IoT Platform", platform_options)

# Connection parameters based on selected platform
if selected_platform:
    st.sidebar.subheader(f"{selected_platform} Connection Parameters")
    
    connection_params = {}
    for param, param_info in config['platforms'][selected_platform]['connection_params'].items():
        # Get the param from environment variables or use the default
        env_var_name = param_info.get('env_var', '')
        default_value = os.getenv(env_var_name, param_info.get('default', ''))
        
        if param_info.get('sensitive', False):
            connection_params[param] = st.sidebar.text_input(
                param_info['label'], 
                value=default_value,
                type="password"
            )
        else:
            connection_params[param] = st.sidebar.text_input(
                param_info['label'], 
                value=default_value
            )

    # Connect button
    if st.sidebar.button("Connect"):
        with st.spinner(f"Connecting to {selected_platform}..."):
            try:
                # Create platform instance
                platform_factory = IoTPlatformFactory()
                platform = platform_factory.create_platform(selected_platform, connection_params)
                
                # Test connection
                if platform.test_connection():
                    st.session_state.connected = True
                    st.session_state.platform = platform
                    st.session_state.sensors = platform.discover_sensors()
                    st.success(f"Successfully connected to {selected_platform}!")
                else:
                    st.error(f"Failed to connect to {selected_platform}. Please check your credentials.")
            except Exception as e:
                st.error(f"Error connecting to platform: {str(e)}")

# Disconnect button if connected
if st.session_state.connected:
    if st.sidebar.button("Disconnect"):
        st.session_state.connected = False
        st.session_state.platform = None
        st.session_state.sensors = []
        st.session_state.selected_sensors = []
        st.rerun()

# Main dashboard area
st.title("IoT Sensor Dashboard")

# Display connection status
if st.session_state.connected:
    st.success(f"Connected to {selected_platform}")
    
    # Sensors selection
    st.subheader("Available Sensors")
    
    if st.session_state.sensors:
        # Create columns for sensor selection
        cols = st.columns(3)
        selected_sensors = []
        
        for i, sensor in enumerate(st.session_state.sensors):
            col_idx = i % 3
            with cols[col_idx]:
                if st.checkbox(f"{sensor['name']} ({sensor['type']})", 
                               key=f"sensor_{i}",
                               value=sensor in st.session_state.selected_sensors):
                    selected_sensors.append(sensor)
        
        st.session_state.selected_sensors = selected_sensors
    else:
        st.info("No sensors detected. Please check your connection or device configuration.")
    
    # Data visualization section
    if st.session_state.selected_sensors:
        st.subheader("Sensor Data Visualization")
        
        # Time range selection
        time_options = {
            "Last 15 minutes": 15,
            "Last hour": 60,
            "Last 3 hours": 180,
            "Last 12 hours": 720,
            "Last 24 hours": 1440
        }
        selected_time = st.selectbox("Select time range", list(time_options.keys()))
        time_range_minutes = time_options[selected_time]
        
        # Create tabs for real-time and historical data
        tab1, tab2, tab3 = st.tabs(["Real-time Data", "Historical Data", "Alerts"])
        
        with tab1:
            st.write("Real-time sensor readings (refreshes automatically)")
            
            # Create a placeholder for real-time data
            real_time_container = st.empty()
            
            # Auto-refresh every 5 seconds (this is for demonstration - in production you might use MQTT websockets)
            with real_time_container.container():
                for sensor in st.session_state.selected_sensors:
                    st.write(f"### {sensor['name']} ({sensor['type']})")
                    
                    # Get latest data for the sensor
                    try:
                        if st.session_state.platform:
                            latest_data = st.session_state.platform.get_latest_data(sensor['id'])
                            st.session_state.data_handler.save_sensor_data(sensor['id'], latest_data)
                            
                            # Check alerts for this sensor data
                            alerts = st.session_state.alert_system.check_alerts(sensor, latest_data)
                            if alerts:
                                for alert in alerts:
                                    st.warning(f"⚠️ ALERT: {alert}")
                                    # Add to alerts list if not already there
                                    if alert not in [a['message'] for a in st.session_state.alerts]:
                                        st.session_state.alerts.append({
                                            'sensor': sensor['name'],
                                            'message': alert,
                                            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        })
                            
                            # Create visualization based on sensor type
                            if sensor['type'] in ('temperature', 'humidity', 'pressure'):
                                create_gauge_chart(latest_data, sensor['type'])
                            elif sensor['type'] in ('motion', 'occupancy'):
                                st.write(f"Current status: {'Active' if latest_data['value'] else 'Inactive'}")
                            else:
                                st.write(f"Current value: {latest_data['value']} {latest_data.get('unit', '')}")
                            
                            # Show last updated time
                            st.caption(f"Last updated: {latest_data['timestamp']}")
                        else:
                            st.warning("Platform connection lost. Please reconnect.")
                    except Exception as e:
                        st.error(f"Error fetching data: {str(e)}")
                
                # Auto-refresh (this will be better implemented with WebSockets in production)
                time.sleep(5)
                st.rerun()
        
        with tab2:
            st.write("Historical data analysis")
            
            # Get data for the selected time range
            end_time = datetime.now()
            start_time = end_time - timedelta(minutes=time_range_minutes)
            
            # Select a sensor for historical data
            selected_sensor_for_history = st.selectbox(
                "Select sensor for historical data",
                options=[s['name'] for s in st.session_state.selected_sensors],
                key="history_sensor_select"
            )
            
            # Find the selected sensor object
            selected_sensor_obj = next(
                (s for s in st.session_state.selected_sensors if s['name'] == selected_sensor_for_history), 
                None
            )
            
            if selected_sensor_obj:
                try:
                    # Get historical data
                    historical_data = st.session_state.platform.get_historical_data(
                        selected_sensor_obj['id'], 
                        start_time, 
                        end_time
                    )
                    
                    if historical_data:
                        # Convert to DataFrame
                        df = pd.DataFrame(historical_data)
                        
                        # Display statistics
                        stats_cols = st.columns(4)
                        create_stats_summary(df, stats_cols)
                        
                        # Line chart for historical data
                        st.subheader(f"{selected_sensor_for_history} - Historical Data")
                        create_line_chart(df, selected_sensor_obj['type'])
                        
                        # Show raw data if requested
                        if st.checkbox("Show raw data"):
                            st.dataframe(df)
                    else:
                        st.info(f"No historical data available for {selected_sensor_for_history} in the selected time range.")
                except Exception as e:
                    st.error(f"Error fetching historical data: {str(e)}")
            else:
                st.warning("Please select a sensor first.")
        
        with tab3:
            st.write("Alert Configuration and History")
            
            # Alert configuration section
            st.subheader("Configure Alerts")
            
            # Select sensor for alert configuration
            selected_sensor_for_alert = st.selectbox(
                "Select sensor",
                options=[s['name'] for s in st.session_state.selected_sensors],
                key="alert_sensor_select"
            )
            
            # Find the selected sensor object
            selected_sensor_obj = next(
                (s for s in st.session_state.selected_sensors if s['name'] == selected_sensor_for_alert), 
                None
            )
            
            if selected_sensor_obj:
                # Alert configuration based on sensor type
                alert_type = st.selectbox(
                    "Alert type",
                    options=["Threshold High", "Threshold Low", "Change Rate"],
                    key="alert_type_select"
                )
                
                # Alert threshold
                if alert_type in ["Threshold High", "Threshold Low"]:
                    threshold = st.number_input(
                        "Threshold value",
                        value=0.0,
                        step=0.1,
                        key="alert_threshold"
                    )
                else:  # Change Rate
                    threshold = st.number_input(
                        "Change rate (per minute)",
                        value=0.0,
                        step=0.1,
                        key="alert_rate"
                    )
                
                # Add alert button
                if st.button("Add Alert"):
                    alert_config = {
                        "sensor_id": selected_sensor_obj['id'],
                        "sensor_name": selected_sensor_obj['name'],
                        "type": alert_type,
                        "threshold": threshold
                    }
                    st.session_state.alert_system.add_alert_config(alert_config)
                    st.success(f"Alert configured for {selected_sensor_for_alert}")
            
            # Display current alert configurations
            st.subheader("Current Alert Configurations")
            alert_configs = st.session_state.alert_system.get_alert_configs()
            
            if alert_configs:
                for i, config in enumerate(alert_configs):
                    st.write(f"{i+1}. {config['sensor_name']}: {config['type']} - {config['threshold']}")
                    if st.button(f"Remove", key=f"remove_alert_{i}"):
                        st.session_state.alert_system.remove_alert_config(i)
                        st.rerun()
            else:
                st.info("No alerts configured yet.")
            
            # Display alert history
            st.subheader("Alert History")
            if st.session_state.alerts:
                alert_df = pd.DataFrame(st.session_state.alerts)
                st.dataframe(alert_df)
            else:
                st.info("No alerts triggered yet.")
    else:
        st.info("Please select at least one sensor to view data.")
else:
    # Not connected - show welcome message
    st.markdown("""
    ## Welcome to the IoT Sensor Dashboard

    This application allows you to connect to various IoT platforms, monitor sensor data in real-time, 
    analyze historical trends, and set up alerts for important events.

    ### Supported IoT Platforms:
    - AWS IoT Core
    - Azure IoT Hub
    - Google Cloud IoT
    - ThingSpeak
    - MQTT Brokers
    - Custom API endpoints

    ### Features:
    - Real-time sensor data visualization
    - Historical data analysis
    - Alert configuration for threshold violations
    - Support for multiple sensor types (temperature, humidity, motion, etc.)

    ### Getting Started:
    1. Select an IoT platform from the sidebar
    2. Enter your connection credentials
    3. Click "Connect" to discover available sensors
    4. Select the sensors you want to monitor
    5. Configure alerts as needed

    Connect to your IoT platform using the sidebar to get started.
    """)
    
    # Display demo image
    st.image("assets/dashboard.svg", use_column_width=True)
