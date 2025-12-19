-- Задание 1
-- Попов Ю.А
-- ИУ7-52Б

CREATE TABLE driver (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    start_date DATE NOT NULL,
    region VARCHAR(100) NOT NULL
);

CREATE TABLE route (
    id SERIAL PRIMARY KEY, -- Я добавил
    driver_id INTEGER NOT NULL,
    trip_date DATE,
    trip_time TIME,
    day_of_week VARCHAR(20),
    event_type INTEGER,
    FOREIGN KEY (driver_id) REFERENCES driver(id)
)


INSERT INTO driver (full_name, birth_date, start_date, region) VALUES
('Ivanov Ivan Ivanovich', '1990-10-20', '2024-02-02', 'Moscow'),
('Petrov Petr Petrovich', '2000-05-15', '2024-10-02', 'Moscow'),
('Stepanov Stepan Stepanovich', '2005-03-03', '2024-03-15', 'Kurskaya oblast'),
('Sidorova Maria Sergeevna', '1985-07-12', '2023-01-10', 'Saint Petersburg'),
('Kuznetsov Alexey Andreevich', '1992-11-30', '2024-05-20', 'Novosibirsk'),
('Volkova Ekaterina Dmitrievna', '1998-03-18', '2024-06-01', 'Yekaterinburg'),
('Fedorova Ekaterina Mikhailovna', '1998-06-18', '2023-06-01', 'Nizhnii-Novgorod'),
('Smirnov Dmitry Vladimirovich', '2000-06-05', '2023-12-15', 'Kazan'),
('Morozova Olga Nikolaevna', '1995-01-22', '2024-04-10', 'Sochi'),
('Lebedev Sergey Igorevich', '1991-06-14', '2024-08-05', 'Vladivostok'),
('Nikolaeva Anna Alexandrovna', '1993-12-08', '2024-07-25', 'Rostov-on-Don');

INSERT INTO route (driver_id, trip_date, trip_time, day_of_week, event_type) VALUES
(1, '2025-02-20', '14:00', 'Wensday', 0),
(1, '2025-10-16', '10:00', 'Tuesday', 1),
(1, '2025-10-16', '18:15', 'Monday', 0),
(2, '2025-12-20', '14:00', 'Monday', 0),
(1, '2025-12-25', '12:04', 'Thursday', 1),
(3, '2025-03-15', '08:30', 'Sunday', 0),
(4, '2025-04-05', '09:00', 'Saturday', 1),
(5, '2025-05-10', '16:20', 'Monday', 0),
(6, '2025-06-12', '07:45', 'Thursday', 1),
(7, '2025-07-20', '13:30', 'Sunday', 0);

----------------------------------------------------------------------------------------
-- query plans 1
-- План описывает выполнение запроса. Запрос выбирает первые 4 строки по рангу для каждого водителя, но только для поездок типа route_type = 1.
WITH ranked_routes AS (
    SELECT 
        driver_id,
        trip_date,
        trip_time,
        ROW_NUMBER() OVER (PARTITION BY driver_id ORDER BY trip_date, trip_time) AS rn
    FROM route
    WHERE event_type = 1
)
SELECT driver_id
FROM ranked_routes
WHERE rn = 4;

-- query plans 2
-- Находит водителей у которых меньше двух поездок типа route_type = 1
SELECT driver_id
FROM route
WHERE event_type = 1 
GROUP BY driver_id
HAVING COUNT(*) < 2;