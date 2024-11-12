import random
import time
import os
import json
from confluent_kafka import SerializingProducer
from datetime import datetime, timedelta
from uuid import uuid4, UUID

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
        self.KAFKA_CONFIG=KAFKA_CONFIG
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
            'timestamp': timestamp.isoformat(),
            'latitude': round(location['latitude'], 4),
            'longitude': round(location['longitude'], 4),
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
            'timestamp': timestamp.isoformat(),
            'latitude': round(location['latitude'], 4),
            'longitude': round(location['longitude'], 4),
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
            'timestamp': timestamp.isoformat(),
            'snapshot': "RandomSnapshotFromCamera",
        }

    def generate_weather_data(self):
        location = self.current_cooordinates
        timestamp = self.current_time
        return {
            'id': uuid4(),
            'deviceId': self.device_info['deviceId'],
            'timestamp': timestamp.isoformat(),
            'latitude': round(location['latitude'], 4),
            'longitude': round(location['longitude'], 4),
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
            'timestamp': timestamp.isoformat(),
            'latitude': round(location['latitude'], 4),
            'longitude': round(location['longitude'], 4),
            'incidentId': uuid4(),
            'type': 'None' if incident_rate < 0.9 else random.choice(['Accident', 'Fire', 'Medical', 'Police'])
        }

    def move_vehicle(self):
        # move and update current_time
        self.current_cooordinates['latitude'] += self.lat_step + random.uniform(-0.0005, 0.0005)
        self.current_cooordinates['longitude'] += self.long_step + random.uniform(-0.0005, 0.0005)
        self.current_time += timedelta(seconds=random.randint(30, 60))

    def json_serializer(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")    

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()}')

    def produce_to_kafka(self, producer, topic, data):
        producer.produce(
            topic,
            key=str(data['id']),
            value=json.dumps(data, default=self.json_serializer).encode('utf-8'),
            on_delivery=self.delivery_report,
        )
        producer.flush()

    def make_simulate(self):
        for step in range(self.steps):
            self.move_vehicle()
            
            # generating data
            vehicle_data = self.generate_vehicle_data()
            gps_data = self.generate_gps_data()
            camera_data = self.generate_camera_data()
            weather_data = self.generate_weather_data()
            emergency_incident_data = self.generate_emergency_incident()

            # producting data to topics
            self.produce_to_kafka(self.producer, self.KAFKA_CONFIG['VEHICLE_TOPIC'], vehicle_data)
            self.produce_to_kafka(self.producer, self.KAFKA_CONFIG['GPS_TOPIC'], gps_data)
            self.produce_to_kafka(self.producer, self.KAFKA_CONFIG['CAMERA_TOPIC'], camera_data)
            self.produce_to_kafka(self.producer, self.KAFKA_CONFIG['WEATHER_TOPIC'], weather_data)
            self.produce_to_kafka(self.producer, self.KAFKA_CONFIG['EMERGENCY_TOPIC'], emergency_incident_data)

            # continue send data after 1s
            time.sleep(1)