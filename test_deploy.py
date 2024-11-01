import paho.mqtt.client as mqtt
import json
import time
import numpy as np
from datetime import datetime

# MQTT setup
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# Add these constants at the start of the script
BASE_FREQ = 0.5  # Base frequency in Hz
TIME_OFFSET = 0.04  # 2 iterations (at 50Hz) worth of lag
# Random phase offsets for each servo (generated once)
position_offsets = np.random.uniform(0, 2*np.pi, 16)
velocity_offsets = np.random.uniform(0, 2*np.pi, 16)
# Random amplitude modifiers for each servo
position_amplitudes = np.random.uniform(120, 180, 16)  # Different amplitude for each servo
velocity_amplitudes = np.random.uniform(30, 50, 16)

try:
    while True:
        # Current timestamp
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Current time for sine wave calculation
        t = time.time()
        t_desired = t + TIME_OFFSET  # Desired values lead actual values
        
        # Generate sine waves for actual positions
        positions = {
            str(i+1): amp * np.sin(2*np.pi*BASE_FREQ*t + offset)
            for i, (amp, offset) in enumerate(zip(position_amplitudes, position_offsets))
        }
        
        # Generate sine waves for desired positions (offset in time)
        positions_desired = {
            str(i+1)+"_desired": amp * np.sin(2*np.pi*BASE_FREQ*t_desired + offset)
            for i, (amp, offset) in enumerate(zip(position_amplitudes, position_offsets))
        }
        
        # Generate sine waves for actual velocities
        velocities = {
            str(i+1): amp * np.sin(2*np.pi*BASE_FREQ*t + offset)
            for i, (amp, offset) in enumerate(zip(velocity_amplitudes, velocity_offsets))
        }
        
        # Generate sine waves for desired velocities (offset in time)
        velocities_desired = {
            str(i+1)+"_desired": amp * np.sin(2*np.pi*BASE_FREQ*t_desired + offset)
            for i, (amp, offset) in enumerate(zip(velocity_amplitudes, velocity_offsets))
        }
        
        # Generate sinusoidal IMU data
        imu_data = {
            "accel": {
                "x": np.sin(2*np.pi*0.3*t),
                "y": np.sin(2*np.pi*0.3*t + np.pi/3),
                "z": 10 + 0.5*np.sin(2*np.pi*0.3*t + np.pi/2)  # Oscillate around 10
            },
            "gyro": {
                "x": 5*np.sin(2*np.pi*0.4*t),
                "y": 5*np.sin(2*np.pi*0.4*t + np.pi/3),
                "z": 5*np.sin(2*np.pi*0.4*t + 2*np.pi/3)
            },
            "euler": {
                "x": 90*np.sin(2*np.pi*0.2*t),
                "y": 90*np.sin(2*np.pi*0.2*t + np.pi/3),
                "z": 90*np.sin(2*np.pi*0.2*t + 2*np.pi/3)
            }
        }
        
        # Combine all data
        data = {
            "time": timestamp,
            "servo_positions": positions,
            "servo_positions_desired": positions_desired,
            "servo_velocities": velocities,
            "servo_velocities_desired": velocities_desired,
            "imu": imu_data
        }
        
        # Publish to MQTT
        client.publish("robot/control", json.dumps(data))
        
        # Sleep for 20ms (50Hz)
        time.sleep(0.02)

except KeyboardInterrupt:
    print("Stopping data simulation")
    client.disconnect()
