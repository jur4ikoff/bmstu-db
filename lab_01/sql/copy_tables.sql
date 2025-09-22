COPY Car(id, vin_number, registration_plate, brand, model, mileage) FROM '/data/cars.csv' delimiter ';'; 
COPY Driver(id, car_id, first_name, last_name, experience, score, date_of_birthday, address, document_number) FROM '/data/drivers.csv' delimiter ';';
COPY Passenger(id, first_name, last_name, date_of_birthday, address) FROM '/data/passengers.csv' delimiter ';';
COPY Payment(id, invoice, status) FROM '/data/payments.csv' delimiter ';';
COPY Trip(id, driver_id, passenger_id, payment_id, source_address, destenation_address, price, score) FROM '/data/trips.csv' delimiter ';';