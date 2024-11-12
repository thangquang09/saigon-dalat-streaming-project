import os

SAIGON_COORDINATES = {
    'latitude': 10.8231,
    'longitude': 106.6297
}

DALAT_COORDINATES = {
    'latitude': 11.9404,
    'longitude': 108.4583
}

KAFKA_BOOTSTRAP_SERVERS =  os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
WEATHER_TOPIC =  os.getenv('WEATHER_TOPIC', 'weather_data')
GPS_TOPIC =  os.getenv('GPS_TOPIC', 'gps_data')
CAMERA_TOPIC =  os.getenv('CAMERA_TOPIC', 'camera_data')
EMERGENCY_TOPIC =  os.getenv('EMERGENCY_TOPIC', 'emergency_data')

KAFKA_CONFIG = {
    "KAFKA_BOOTSTRAP_SERVERS": KAFKA_BOOTSTRAP_SERVERS,
    "VEHICLE_TOPIC": VEHICLE_TOPIC,
    "WEATHER_TOPIC": WEATHER_TOPIC,
    "GPS_TOPIC": GPS_TOPIC,
    "CAMERA_TOPIC": CAMERA_TOPIC,
    "EMERGENCY_TOPIC": EMERGENCY_TOPIC,
}

HDFS_NAMENODE = "hdfs://namenode:9000"