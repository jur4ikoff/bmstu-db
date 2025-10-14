CREATE TABLE IF NOT EXISTS Car
(
    id SERIAL,
    vin_number VARCHAR(15),
    registration_plate VARCHAR(15),
    brand VARCHAR(31),
    model VARCHAR(31),
    mileage INTEGER
);

CREATE TABLE IF NOT EXISTS Driver
(
    id SERIAL,
    car_id INTEGER,
    first_name VARCHAR(63), 
    last_name VARCHAR(63),
    experience SMALLINT,
    score NUMERIC,
    date_of_birthday DATE,
    address VARCHAR(128),
    document_number BIGINT
);

CREATE TABLE IF NOT EXISTS Passenger
(
    id SERIAL,
    first_name VARCHAR(63),
    last_name VARCHAR(63),
    date_of_birthday DATE,
    address VARCHAR(127)
);


CREATE TABLE IF NOT EXISTS Payment
(
    id SERIAL,
    invoice INTEGER,
    status BOOL
);

CREATE TABLE IF NOT EXISTS Trip
(
    id SERIAL,
    driver_id INTEGER,
    passenger_id INTEGER,
    payment_id BIGINT,
    source_address VARCHAR(128),
    destenation_address VARCHAR(128),
    price INTEGER,
    score INTEGER
);

