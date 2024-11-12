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
            'speed': random.randint(20, 60), # km/h
            'controlPlate': self.device_info['controlPlate'],
            'deviceType': self.device_info['deviceType'],
            'model': self.device_info['model'],
            'year': self.device_info['year'],
        }

    

    def move_vehicle(self):
        # move and update current_time
        self.current_cooordinates['latitude'] += self.lat_step + random.uniform(-0.0005, 0.0005)
        self.current_cooordinates['longitude'] += self.long_step + random.uniform(-0.0005, 0.0005)
        self.current_time += timedelta(seconds=random.randint(30, 60))

    def make_simulate(self):
        for step in range(self.steps):
            self.move_vehicle()
            vehicle_data = self.generate_vehicle_data()
            print(vehicle_data)

            time.sleep(1.5)
        
        print(f"Vehicle moved from {self.start_location} to {self.end_location}")



# def procedureKafka(data):
#     # flush
#     pass

# def streamKafka():
#     while True:
#         print("streaming...")
#         break
