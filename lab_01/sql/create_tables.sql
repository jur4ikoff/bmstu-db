CREATE TABLE if not EXISTS Driver
(
    driver_id SERIAL PRIMARY KEY,
    car_id INTEGER,
    first_name VARCHAR(63), 
    last_name VARCHAR(63),
    experience INTEGER,
    score FLOAT,
    date_of_birthday VARCHAR(10),
    adress VARCHAR(128),
    document_number INTEGER
);
