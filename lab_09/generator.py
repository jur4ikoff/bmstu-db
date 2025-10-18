from gen_models import GenDriver, GenTrip, GenCar, GenPassenger, GenPayment

import os
import csv


GENERATE_COUNT = 10


def generate_csv(model, filename: str):
    """Функция для генерации csv файлов"""
    if os.path.exists(filename):
        os.remove(filename)

    car_id_list = list(range(1, GENERATE_COUNT + 1))
    payment_id_list = list(range(1, GENERATE_COUNT + 1))

    SHIFT = 1000
    with open(file=filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(model.headers())
        for i in range(GENERATE_COUNT):

            if model == GenCar:
                generate_model = model.generate(primary_key=i + SHIFT + 1)
            elif model == GenDriver:
                generate_model = model.generate(
                    primary_key=i + SHIFT + 1, secondary_key=car_id_list
                )
            elif model == GenTrip:
                generate_model = model.generate(
                    id=i + SHIFT + 1, payment_id=payment_id_list
                )
            else:
                generate_model = model.generate(primary_key=i + SHIFT + 1)

            line = generate_model.to_list()
            writer.writerow(line)
