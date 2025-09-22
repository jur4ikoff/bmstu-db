from models import Driver, Trip, Car, Passenger, Payment

import os
import csv


GENERATE_COUNT = 1000

def generate_csv(model, filename: str):
    """Функция для генерации csv файлов"""
    if os.path.exists(filename):
        os.remove(filename)

    car_id_list = list(range(1, GENERATE_COUNT + 1))
    with open(file=filename, mode="w", newline="", encoding="utf-8") as file:
        for i in range(GENERATE_COUNT):
            
            
            if model == Car:
                generate_model = model.generate(primary_key=i + 1)
            elif model == Driver:
                generate_model = model.generate(primary_key=i + 1, secondary_key=car_id_list)
            else:
                generate_model = model.generate(primary_key=i + 1)

                
            line = generate_model.to_list()

            writer = csv.writer(file, delimiter=";")
            writer.writerow(line)

