import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

def create_line_chart(data, sensor_type=None):
    """Create a line chart for sensor data"""
    # Convert to DataFrame if it's a list of dictionaries
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    
    # Ensure timestamp is properly formatted
    if 'timestamp' in df.columns:
        if isinstance(df['timestamp'].iloc[0], str):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Determine y-axis label based on sensor type and unit
    if 'unit' in df.columns:
        y_label = f"Value ({df['unit'].iloc[0]})"
    elif sensor_type:
        units = {
            'temperature': '°C',
            'humidity': '%',
            'pressure': 'hPa',
            'co2': 'ppm',
            'light': 'lux',
            'motion': 'activity',
            'occupancy': 'count'
        }
        y_label = f"{sensor_type.capitalize()} ({units.get(sensor_type, 'value')})"
    else:
        y_label = "Value"
    
    # Create the line chart
    fig = px.line(
        df, 
        x='timestamp', 
        y='value',
        title=f"Sensor Readings Over Time",
        labels={'timestamp': 'Time', 'value': y_label}
    )
    
    # Customize the chart
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified"
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    return fig


def create_gauge_chart(data, sensor_type=None):
    """Create a gauge chart for the current sensor value"""
    if isinstance(data, dict):
        value = data.get('value', 0)
        unit = data.get('unit', '')
    else:
        value = data
        unit = ''
    
    # Define ranges based on sensor type
    if sensor_type == 'temperature':
        min_val, max_val = 0, 40
        thresholds = [
            {'min': 0, 'max': 15, 'color': 'blue'},
            {'min': 15, 'max': 25, 'color': 'green'},
            {'min': 25, 'max': 40, 'color': 'red'}
        ]
        title = 'Temperature'
        if not unit:
            unit = '°C'
    elif sensor_type == 'humidity':
        min_val, max_val = 0, 100
        thresholds = [
            {'min': 0, 'max': 30, 'color': 'yellow'},
            {'min': 30, 'max': 70, 'color': 'green'},
            {'min': 70, 'max': 100, 'color': 'blue'}
        ]
        title = 'Humidity'
        if not unit:
            unit = '%'
    elif sensor_type == 'pressure':
        min_val, max_val = 900, 1100
        thresholds = [
            {'min': 900, 'max': 970, 'color': 'red'},
            {'min': 970, 'max': 1030, 'color': 'green'},
            {'min': 1030, 'max': 1100, 'color': 'red'}
        ]
        title = 'Pressure'
        if not unit:
            unit = 'hPa'
    else:
        min_val, max_val = 0, 100
        thresholds = [
            {'min': 0, 'max': 33, 'color': 'red'},
            {'min': 33, 'max': 66, 'color': 'yellow'},
            {'min': 66, 'max': 100, 'color': 'green'}
        ]
        title = sensor_type.capitalize() if sensor_type else 'Value'
    
    # Create steps for gauge chart
    steps = []
    for threshold in thresholds:
        steps.append(
            dict(
                range=[threshold['min'], threshold['max']],
                color=threshold['color'],
                thickness=0.75
            )
        )
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{title}", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': steps,
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_val * 0.8
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    return fig


def create_bar_chart(data, x_column, y_column, title=None):
    """Create a bar chart from data"""
    # Convert to DataFrame if it's a list of dictionaries
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    
    # Create the bar chart
    fig = px.bar(
        df, 
        x=x_column, 
        y=y_column,
        title=title or f"{y_column} by {x_column}"
    )
    
    # Customize the chart
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    return fig


def create_stats_summary(data, columns=None):
    """Create a statistical summary display"""
    # Convert to DataFrame if it's a list of dictionaries
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    
    # Calculate statistics
    stats = {
        'Min': df['value'].min(),
        'Max': df['value'].max(),
        'Average': df['value'].mean(),
        'Median': df['value'].median()
    }
    
    # If columns are provided, display in those columns
    if columns:
        for i, (stat_name, stat_value) in enumerate(stats.items()):
            if i < len(columns):
                with columns[i]:
                    st.metric(label=stat_name, value=f"{stat_value:.2f}")
    else:
        # Otherwise create a new set of columns
        cols = st.columns(len(stats))
        for i, (stat_name, stat_value) in enumerate(stats.items()):
            with cols[i]:
                st.metric(label=stat_name, value=f"{stat_value:.2f}")
    
    return stats


def create_heatmap(data, x_column, y_column, value_column, title=None):
    """Create a heatmap from data"""
    # Convert to DataFrame if it's a list of dictionaries
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    
    # Create the heatmap
    fig = px.density_heatmap(
        df, 
        x=x_column, 
        y=y_column,
        z=value_column,
        title=title or f"Heatmap of {value_column}"
    )
    
    # Customize the chart
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    return fig


def create_scatter_plot(data, x_column, y_column, color_column=None, title=None):
    """Create a scatter plot from data"""
    # Convert to DataFrame if it's a list of dictionaries
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    
    # Create the scatter plot
    fig = px.scatter(
        df, 
        x=x_column, 
        y=y_column,
        color=color_column,
        title=title or f"{y_column} vs {x_column}"
    )
    
    # Customize the chart
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    return fig
