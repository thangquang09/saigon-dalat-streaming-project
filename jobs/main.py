import os
from simulator import Simulator

SAIGON_COORDINATES = {
    'latitude': 10.8231,
    'longitude': 106.6297
}

DALAT_COORDINATES = {
    'latitude': 11.9404,
    'longitude': 108.4583
}

KAFKA_BOOTSTRAP_SERVERS = "1" #os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = "2" #os.getenv('VEHICLE_TOPIC', 'vehicle_data')

KAFKA_CONFIG = {
    "KAFKA_BOOTSTRAP_SERVERS": KAFKA_BOOTSTRAP_SERVERS,
    "VEHICLE_TOPIC": VEHICLE_TOPIC,
}

device_info = {
    "deviceId": 1,
    "controlPlate": "49H1-00922",
    "deviceType": "Toyota",
    "model": "Camry",
    "year": 2012,
}

new_simulator1 = Simulator(SAIGON_COORDINATES, DALAT_COORDINATES, "Sai Gon", 3, device_info, KAFKA_CONFIG)
new_simulator2 = Simulator(DALAT_COORDINATES, SAIGON_COORDINATES, "Da Lat", 3, device_info, KAFKA_CONFIG)

new_simulator1.make_simulate()
new_simulator2.make_simulate()