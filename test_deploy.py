import paho.mqtt.client as mqtt
import json
import time
import numpy as np
from datetime import datetime

# MQTT setup
client = mqtt.Client()
client.connect("localhost", 1883, 60)

try:
    while True:
        # Current timestamp
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Simulate 16 servo positions (roughly -180 to +180 degrees)
        positions = {str(i+1): pos for i, pos in enumerate(np.random.uniform(-180, 180, 16).tolist())}
        
        # Simulate 16 servo velocities (-50 to +50 deg/s)
        velocities = {str(i+1): vel for i, vel in enumerate(np.random.uniform(-50, 50, 16).tolist())}
        # Simulate IMU data
        imu_data = {
            "accel": {
                "x": np.random.uniform(-2, 2),
                "y": np.random.uniform(-2, 2),
                "z": np.random.uniform(9.5, 10.5)  # Roughly 1G + noise
            },
            "gyro": {
                "x": np.random.uniform(-10, 10),
                "y": np.random.uniform(-10, 10),
                "z": np.random.uniform(-10, 10)
            }, 
            "euler": {
                "x": np.random.uniform(-180, 180),
                "y": np.random.uniform(-180, 180),
                "z": np.random.uniform(-180, 180)
            }
        }
        
        # Combine all data
        data = {
            "time": timestamp,
            "servo_positions": positions,
            "servo_velocities": velocities,
            "imu": imu_data
        }
        
        # Publish to MQTT
        client.publish("robot/control", json.dumps(data))
        
        # Sleep for 20ms (50Hz)
        time.sleep(0.02)

except KeyboardInterrupt:
    print("Stopping data simulation")
    client.disconnect()
