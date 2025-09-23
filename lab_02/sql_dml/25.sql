-- 25. Оконные фнкции для устранения дублей
-- Придумать запрос, в результате которого в данных появляются полные дубли.
-- Устранить дублирующиеся строки с использованием функции ROW_NUMBER().

-- Создание дубликатов
-- INSERT INTO Trip (driver_id, passenger_id, source_address, destenation_address, price, score)
-- VALUES 
-- (1, 1, 'ул. Ленина, 1', 'ул. Пушкина, 2', 300, 5),
-- (1, 1, 'ул. Ленина, 1', 'ул. Пушкина, 2', 300, 5), 
-- (1, 1, 'ул. Ленина, 1', 'ул. Пушкина, 2', 300, 5); 

--  Вывод дубликатов на экран
-- SELECT 
--     id,
--     driver_id,
--     source_address,
--     price,
--     ROW_NUMBER() OVER (PARTITION BY driver_id, source_address, price ORDER BY id) as row_num
-- FROM Trip;

-- Удаление дубликатов, с помощью ROW_NUMBER()
DELETE FROM Trip 
WHERE id IN (
    SELECT id
    FROM (
        SELECT 
            id,
            ROW_NUMBER() OVER (PARTITION BY driver_id, source_address, price ORDER BY id) as row_num
        FROM Trip
    ) as numbered
    WHERE row_num > 1
);