import random
import time
import os
from confluent_kafka import SerializingProducer
from datetime import datetime, timedelta
from uuid import uuid4

class Simulator:

    def __init__(self, start_cooordinates, end_cooordinates, start_location, steps, device_info, KAFKA_CONFIG):
        self.start_cooordinates = start_cooordinates
        self.end_cooordinates = end_cooordinates
        self.current_cooordinates = start_cooordinates
        self.steps = steps
        self.start_location = start_location
        self.current_time = datetime.now()
        self.lat_step = (end_cooordinates['latitude'] - start_cooordinates['latitude']) / steps
        self.long_step = (end_cooordinates['longitude'] - start_cooordinates['longitude']) / steps
        self.start_location = start_location
        self.end_location = "Da Lat" if start_location == "Sai Gon" else "Sai Gon"
        self.device_info = device_info
        self.producer_config = {
            'bootstrap.servers': KAFKA_CONFIG['KAFKA_BOOTSTRAP_SERVERS'],
            'error_cb': lambda err: print(f'Kafka error: {err}')
        }
        self.producer = SerializingProducer(self.producer_config)

    def generate_vehicle_data(self):
        location = self.current_cooordinates
        timestamp = self.current_time
        return {
            'id': uuid4(),
            'deviceId': self.device_info['deviceId'],
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'location': (location['latitude'], location['longitude']),
            'controlPlate': self.device_info['controlPlate'],
            'deviceType': self.device_info['deviceType'],
            'model': self.device_info['model'],
            'year': self.device_info['year'],
        }

    def generate_gps_data(self):
        location = self.current_cooordinates
        timestamp = self.current_time
        return {
            'id': uuid4(),
            'deviceId': self.device_info['deviceId'],
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'location': (location['latitude'], location['longitude']),
            'speed': random.uniform(20, 60), # km/h
            'direction': random.randint(0, 360),
            'accuracy': "+-" + str(random.randint(2, 7)) + "m",
            'satelliteCount': random.randint(2, 5),
        }

    def generate_camera_data(self):
        timestamp = self.current_time
        return {
            'id': uuid4(),
            'deviceId': self.device_info['deviceId'],
            'cameraId': random.choice(self.device_info['cameraId']),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'snapshot': "RandomSnapshotFromCamera",
        }

    def generate_weather_data(self):
        location = self.current_cooordinates
        timestamp = self.current_time
        return {
            'id': uuid4(),
            'deviceId': self.device_info['deviceId'],
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'location': (location['latitude'], location['longitude']),
            'temperature': round(random.uniform(20, 30), 1),
            'humidity': random.randint(50, 80),
            'windSpeed': round(random.uniform(0, 100), 1),
            'weatherCondition': random.choice(['Sunny', 'Cloudy', 'Rainy'])
        }

    def generate_emergency_incident(self):
        location = self.current_cooordinates
        timestamp = self.current_time
        incident_rate = random.uniform(0, 1) # 90% safety :v
        return {
            'id': uuid4(),
            'deviceId': self.device_info['deviceId'],
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'location': (location['latitude'], location['longitude']),
            'incidentId': uuid4(),
            'type': 'None' if incident_rate < 0.9 else random.choice(['Accident', 'Fire', 'Medical', 'Police'])
        }

    def move_vehicle(self):
        # move and update current_time
        self.current_cooordinates['latitude'] += self.lat_step + random.uniform(-0.0005, 0.0005)
        self.current_cooordinates['longitude'] += self.long_step + random.uniform(-0.0005, 0.0005)
        self.current_time += timedelta(seconds=random.randint(30, 60))

    def produce_to_kafka(self, producer, topic, data):
        pass

    def make_simulate(self):
        for step in range(self.steps):
            self.move_vehicle()
            vehicle_data = self.generate_vehicle_data()
            gps_data = self.generate_gps_data()
            camera_data = self.generate_camera_data()
            weather_data = self.generate_weather_data()
            emergency_incident_data = self.generate_emergency_incident()

        # # call streaming data to kafka later
        #     print(vehicle_data, file=file)
        #     print(gps_data, file=file)
        #     print(camera_data, file=file)
        #     print(weather_data, file=file)
        #     print(emergency_incident_data, file=file)
            time.sleep(1.5)
        
        print(f"Vehicle moved from {self.start_location} to {self.end_location}")