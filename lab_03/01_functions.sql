-- Написать 4 функции
-- • Скалярную функцию
-- • Подставляемую табличную функцию
-- • Многооператорную табличную функцию
-- • Рекурсивную функцию или функцию с рекурсивным ОТВ

--------------------------------------------------------
-- Скалярная функцию
-- AGE вычисляет разницу между тек датой и ДР
-- EXTRACT - извлекает кол-во лет
CREATE OR REPLACE FUNCTION calculate_avg_driver_age()
RETURNS NUMERIC AS $$
DECLARE
    avg_age NUMERIC;
BEGIN
    SELECT AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birthday)))
    INTO avg_age
    FROM Driver;
    
    RETURN ROUND(avg_age, 2);
END;
$$ LANGUAGE plpgsql;

SELECT calculate_avg_driver_age() AS average_driver_age;

-------------------------------------------------------
-- Подставляемая табличная функция
CREATE OR REPLACE FUNCTION get_trips_by_price_range(
    min_price INTEGER DEFAULT 0,
    max_price INTEGER DEFAULT 1000
)
RETURNS TABLE(
    trip_id INTEGER,
    driver_name VARCHAR,
    passenger_name VARCHAR,
    source_addr VARCHAR,
    dest_addr VARCHAR,
    trip_price INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        (d.first_name || ' ' || d.last_name)::VARCHAR,
        (p.first_name || ' ' || p.last_name)::VARCHAR,
        t.source_address,
        t.destenation_address,
        t.price
    FROM Trip t
    JOIN Driver d ON t.driver_id = d.id
    JOIN Passenger p ON t.passenger_id = p.id
    WHERE t.price BETWEEN min_price AND max_price
    ORDER BY t.price DESC;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_trips_by_price_range(1000, 5000);


-------------------------------------------------------
-- Многооператорная табличную функцию
CREATE OR REPLACE FUNCTION analyze_drivers()
RETURNS TABLE(
    driver_id INTEGER,
    full_name VARCHAR,
    experience_level VARCHAR,
    rating_category VARCHAR,
    car_info VARCHAR
) AS $$
DECLARE
    driver_record RECORD;
BEGIN
    CREATE TEMP TABLE temp_driver_analysis (
        driver_id INTEGER,
        full_name VARCHAR(127),
        experience_level VARCHAR(20),
        rating_category VARCHAR(20),
        car_info VARCHAR(63)
    );
    
    -- Заполняем временную таблицу данными
    FOR driver_record IN 
        SELECT 
            d.id,
            d.first_name || ' ' || d.last_name as full_name,
            d.experience,
            d.score,
            c.brand || ' ' || c.model as car_model
        FROM Driver d
        LEFT JOIN Car c ON d.car_id = c.id
    LOOP
        -- Определяем уровень опыта
        INSERT INTO temp_driver_analysis
        VALUES (
            driver_record.id,
            driver_record.full_name,
            CASE 
                WHEN driver_record.experience < 2 THEN 'Новичок'
                WHEN driver_record.experience BETWEEN 2 AND 5 THEN 'Опытный'
                ELSE 'Профессионал'
            END,
            CASE 
                WHEN driver_record.score < 4.0 THEN 'Низкий'
                WHEN driver_record.score BETWEEN 4.0 AND 4.7 THEN 'Средний'
                ELSE 'Высокий'
            END,
            COALESCE(driver_record.car_model, 'Без автомобиля')
        );
    END LOOP;
    
    -- Возвращаем результаты
    RETURN QUERY SELECT * FROM temp_driver_analysis;
    
    -- Очищаем временную таблицу
    DROP TABLE temp_driver_analysis;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM analyze_drivers();

------------------------------------------------------------------
-- • Рекурсивную функцию или функцию с рекурсивным ОТВ
CREATE OR REPLACE FUNCTION simple_trip_hierarchy(start_trip_id INTEGER)
RETURNS TABLE(
    level INTEGER,
    trip_id INTEGER,
    source_address VARCHAR,
    destination_address VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    WITH RECURSIVE trip_tree AS (
        -- Базовый случай
        SELECT 
            t.id,
            t.source_address,
            t.destenation_address,
            0 as level
        FROM Trip t
        WHERE t.id = start_trip_id
        
        UNION ALL
        
        -- Рекурсивный случай
        SELECT 
            t.id,
            t.source_address,
            t.destenation_address,
            tt.level + 1
        FROM Trip t
        INNER JOIN trip_tree tt ON t.id = tt.id + 1
        WHERE tt.level < 10 -- Глубина рекурсии
    )
    SELECT 
        tt.level,
        tt.id as trip_id,
        tt.source_address,
        tt.destenation_address as destination_address
    FROM trip_tree tt;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM simple_trip_hierarchy(1);
