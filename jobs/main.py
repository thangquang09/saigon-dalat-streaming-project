from simulator import Simulator
from multiprocessing import Process
from simulator import Simulator
from config import *

device_info = {
    "deviceId": 1,
    "controlPlate": "49H1-00922",
    "deviceType": "Toyota",
    "model": "Camry",
    "year": 2012,
    "cameraId": [1, 2, 3],
}

def start_simulation(start_cooordinates, end_cooordinates, start_name):
    simulator = Simulator(
        start_cooordinates=start_cooordinates,
        end_cooordinates=end_cooordinates,
        start_location=start_name,
        steps=10,
        device_info=device_info,
        KAFKA_CONFIG=KAFKA_CONFIG
    )
    simulator.make_simulate()

def main():
    saigon_coords = {'latitude': 10.8231, 'longitude': 106.6297}
    dalat_coords = {'latitude': 11.9404, 'longitude': 108.4583}

    processes = []

    while True:
        print("\nChương trình điều khiển chuyến đi")
        print("1. Tạo chuyến đi từ Sài Gòn đến Đà Lạt")
        print("2. Tạo chuyến đi từ Đà Lạt về Sài Gòn")
        print("3. Thoát")
        choice = input("Chọn một tùy chọn (1/2/3): ")

        if choice == '1':
            print("Bắt đầu chuyến đi từ Sài Gòn đến Đà Lạt...")
            process = Process(target=start_simulation, args=(saigon_coords, dalat_coords, "Sai Gon"))
            processes.append(process)
            process.start()

        elif choice == '2':
            print("Bắt đầu chuyến đi từ Đà Lạt về Sài Gòn...")
            process = Process(target=start_simulation, args=(dalat_coords, saigon_coords, "Da Lat"))
            processes.append(process)
            process.start()

        elif choice == '3':
            print("Thoát chương trình...")
            break

        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại!")

    # Chờ cho tất cả các tiến trình kết thúc
    for process in processes:
        process.join()
    

if __name__ == "__main__":
    main()