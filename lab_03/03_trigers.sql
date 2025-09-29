-- Триггеры
-- Триггер AFTER
-- Функция для триггера AFTER
CREATE OR REPLACE FUNCTION update_car_mileage()
RETURNS TRIGGER AS $$
BEGIN
    -- Предположим, что каждая поездка добавляет 10 км к пробегу машины
    -- В реальной системе здесь была бы логика расчета расстояния
    UPDATE Car 
    SET mileage = mileage + 10
    WHERE id = (
        SELECT car_id 
        FROM Driver 
        WHERE id = NEW.driver_id
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер AFTER
CREATE TRIGGER after_trip_insert
AFTER INSERT ON Trip
FOR EACH ROW
EXECUTE FUNCTION update_car_mileage();


-- Функция для триггера AFTER
CREATE OR REPLACE FUNCTION update_car_mileage()
RETURNS TRIGGER AS $$
BEGIN
    -- Предположим, что каждая поездка добавляет 10 км к пробегу машины
    -- В реальной системе здесь была бы логика расчета расстояния
    UPDATE Car 
    SET mileage = mileage + 10
    WHERE id = (
        SELECT car_id 
        FROM Driver 
        WHERE id = NEW.driver_id
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер AFTER
CREATE TRIGGER after_trip_insert
AFTER INSERT ON Trip
FOR EACH ROW
EXECUTE FUNCTION update_car_mileage();


-------------------------------------------
--- Тригер INSTEAD OF
-- Создаем представление, которое объединяет водителей и их машины
-- Создаем представление, которое объединяет водителей и их машины
CREATE OR REPLACE VIEW driver_car_view AS
SELECT 
    d.id as driver_id,
    d.first_name,
    d.last_name,
    d.experience,
    c.id as car_id,
    c.brand,
    c.model,
    c.registration_plate
FROM Driver d
LEFT JOIN Car c ON d.car_id = c.id;

-- Функция для триггера INSTEAD OF
CREATE OR REPLACE FUNCTION insert_driver_car()
RETURNS TRIGGER AS $$
BEGIN
    -- Сначала проверяем, существует ли машина
    IF NEW.car_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Car WHERE id = NEW.car_id) THEN
        RAISE EXCEPTION 'Car with id % does not exist', NEW.car_id;
    END IF;
    
    -- Вставляем нового водителя
    INSERT INTO Driver (car_id, first_name, last_name, experience, score, date_of_birthday, address, document_number)
    VALUES (
        NEW.car_id,
        NEW.first_name,
        NEW.last_name,
        COALESCE(NEW.experience, 0),  -- если опыт не указан, ставим 0
        5.0,  -- начальный рейтинг
        CURRENT_DATE,  -- дата рождения по умолчанию
        'Unknown',  -- адрес по умолчанию
        floor(random() * 9000000000 + 1000000000)::bigint  -- случайный номер документа
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер INSTEAD OF для представления
CREATE TRIGGER instead_of_insert_driver
INSTEAD OF INSERT ON driver_car_view
FOR EACH ROW
EXECUTE FUNCTION insert_driver_car();


-- -- Найти имя последовательности (обычно: таблица_id_seq)
-- SELECT pg_get_serial_sequence('car', 'id');

-- -- Сбросить последовательность на максимальный ID + 1
-- SELECT setval(pg_get_serial_sequence('car', 'id'), COALESCE(MAX(id), 0) + 1) FROM trip;
-- -- Вставка через представление (триггер INSTEAD OF обработает эту операцию)

INSERT INTO driver_car_view (first_name, last_name, experience, car_id)
VALUES ('Иван', 'Петров', 3, 1);

SELECT * FROM driver_car_view
WHERE driver_id > 1000