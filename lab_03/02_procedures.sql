------------------------------------------------
-- • Хранимая процедура без параметров или с параметрами
CREATE OR REPLACE PROCEDURE update_driver_score(
    driver_id_param INTEGER,
    new_score NUMERIC
)
AS $$
BEGIN
    UPDATE Driver 
    SET score = new_score 
    WHERE id = driver_id_param;
    
    RAISE NOTICE 'Счет водителя % обновлен до %', driver_id_param, new_score;
END;
$$ LANGUAGE plpgsql;

CALL update_driver_score(1, 4.8);


---------------------------------------------
---- Рекурсивная процедура с ОТВ
CREATE OR REPLACE PROCEDURE show_simple_trip_chain(start_trip_id INTEGER)
AS $$
DECLARE
    rec RECORD;
BEGIN
    RAISE NOTICE 'Цепочка поездок начиная с ID %:', start_trip_id;
    RAISE NOTICE '================================';
    
    -- Простая рекурсивная цепочка поездок по порядку ID
    FOR rec IN (
        WITH RECURSIVE trip_sequence AS (
            -- Базовый случай: начальная поездка
            SELECT 
                id,
                source_address,
                destenation_address,
                price,
                1 as level
            FROM Trip 
            WHERE id = start_trip_id
            
            UNION ALL
            
            -- Рекурсивный случай: следующая поездка (ID + 1)
            SELECT 
                t.id,
                t.source_address,
                t.destenation_address,
                t.price,
                ts.level + 1
            FROM Trip t
            INNER JOIN trip_sequence ts ON t.id = ts.id + 1
            WHERE ts.level < 5  -- Максимум 5 поездок в цепочке
        )
        SELECT 
            level,
            id,
            source_address,
            destenation_address,
            price
        FROM trip_sequence
        ORDER BY level
    )
    LOOP
        RAISE NOTICE 'Уровень %: ID %, % -> % (% руб)',
            rec.level,
            rec.id,
            rec.source_address,
            rec.destenation_address,
            rec.price;
    END LOOP;
    
    RAISE NOTICE '================================';
END;
$$ LANGUAGE plpgsql;

CALL show_simple_trip_chain(1);


-------------------------------------
-- Хранимая процедура с курсором
CREATE OR REPLACE PROCEDURE show_cars_high_mileage(min_mileage INTEGER)
AS $$
DECLARE
    car_record RECORD;
    car_cursor CURSOR FOR 
        SELECT brand, model, mileage 
        FROM Car 
        WHERE mileage > min_mileage 
        ORDER BY mileage DESC;
BEGIN
    RAISE NOTICE 'Автомобили с пробегом больше % км:', min_mileage;
    RAISE NOTICE '--------------------------------';
    
    OPEN car_cursor;
    LOOP
        FETCH car_cursor INTO car_record;
        EXIT WHEN NOT FOUND;
        
        RAISE NOTICE '%-%-% км', 
            car_record.brand, 
            car_record.model, 
            car_record.mileage;
    END LOOP;
    CLOSE car_cursor;
END;
$$ LANGUAGE plpgsql;

CALL show_cars_high_mileage(100000);


---------------------------------------------
-- • Хранимую процедуру доступа к метаданным
CREATE OR REPLACE PROCEDURE show_tables_info()
AS $$
DECLARE
    table_record RECORD;
BEGIN
    RAISE NOTICE 'Таблицы в текущей схеме:';
    RAISE NOTICE '========================';
    
    FOR table_record IN 
        SELECT 
            table_name,
            table_type
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    LOOP
        RAISE NOTICE 'Таблица: %, Тип: %', 
            table_record.table_name, 
            table_record.table_type;
    END LOOP;
    
    RAISE NOTICE '========================';
    RAISE NOTICE 'Всего таблиц: %', 
        (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public');
END;
$$ LANGUAGE plpgsql;

CALL show_tables_info();