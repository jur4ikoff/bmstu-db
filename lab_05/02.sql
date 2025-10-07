-- Шаг 1: Создаём целевую таблицу (если ещё не создана)
CREATE TABLE IF NOT EXISTS driver_restored (
    id SERIAL PRIMARY KEY,
    car_id INTEGER,
    first_name VARCHAR(63) NOT NULL,
    last_name VARCHAR(63) NOT NULL,
    experience SMALLINT,
    score NUMERIC,
    date_of_birthday DATE NOT NULL,
    address VARCHAR(128),
    document_number BIGINT UNIQUE,
    FOREIGN KEY (car_id) REFERENCES car(id),
    CHECK (document_number >= 100000000 AND document_number <= 9999999999)
);

-- Шаг 2: Временная таблица для строк
CREATE TEMP TABLE temp_lines (line TEXT);

-- Шаг 3: Загружаем файл построчно
\copy temp_lines FROM 'json/driver.json';

-- Шаг 4: Вставляем, парся каждую строку как JSON-объект
INSERT INTO driver_restored (
    id,
    car_id,
    first_name,
    last_name,
    experience,
    score,
    date_of_birthday,
    address,
    document_number
)
SELECT
    (line::JSON->>'id')::INTEGER,
    (line::JSON->>'car_id')::INTEGER,
    line::JSON->>'first_name',
    line::JSON->>'last_name',
    (line::JSON->>'experience')::SMALLINT,
    (line::JSON->>'score')::NUMERIC,
    (line::JSON->>'date_of_birthday')::DATE,
    line::JSON->>'address',
    (line::JSON->>'document_number')::BIGINT
FROM temp_lines;


-- SELECT * FROM driver_restored

-- SELECT json_agg(t) AS drivers
-- FROM (
--     SELECT 
--         id,
--         car_id,
--         first_name,
--         last_name,
--         experience,
--         score,
--         date_of_birthday,
--         address,
--         document_number
--     FROM driver
-- ) t;

-- psql -h localhost -p 5430 -U postgres_user -d postgres_db -f 02.sql