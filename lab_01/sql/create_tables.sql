CREATE TABLE if NOT EXISTS Car
(
    id SERIAL PRIMARY KEY,
    vin_number VARCHAR(15),
    registration_plate VARCHAR(15),
    brand VARCHAR(31),
    model VARCHAR(31),
    mileage INTEGER
);

CREATE TABLE if not EXISTS Driver
(
    id SERIAL PRIMARY KEY,
    car_id INTEGER,
    first_name VARCHAR(63), 
    last_name VARCHAR(63),
    experience SMALLINT,
    score NUMERIC,
    date_of_birthday DATE,
    address VARCHAR(128),
    document_number BIGINT UNIQUE
);

CREATE TABLE if not EXISTS Passenger
(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(63),
    last_name VARCHAR(63),
    date_of_birthday DATE,
    address VARCHAR(127)
);


CREATE TABLE if not EXISTS Payment
(
    id SERIAL PRIMARY KEY,
    invoice INTEGER,
    status BOOL
);

CREATE TABLE if not EXISTS Trip
(
    id SERIAL PRIMARY KEY,
    driver_id INTEGER,
    passenger_id INTEGER,
    payment_id BIGINT,
    source_address VARCHAR(128),
    destenation_address VARCHAR(128),
    price INTEGER,
    score INTEGER,

    FOREIGN KEY (driver_id) REFERENCES Driver (id),
    FOREIGN KEY (passenger_id) REFERENCES Passenger (id)
);