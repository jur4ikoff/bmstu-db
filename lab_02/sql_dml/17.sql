-- 17. Многострочная инструкция INSERT, выполняющая вставку
-- в таблицу результирующего набора данных вложенного подзапроса
-- Сброс последовательности на следующий ID после максимального
SELECT setval('car_id_seq', (SELECT MAX(id) FROM Car));

INSERT INTO Car (brand, model, mileage)
SELECT 
    brand,
    model,
    (SELECT MAX(mileage) FROM Car WHERE brand = c.brand)
FROM Car c
WHERE c.brand = 'Toyota'
  AND c.mileage IS NOT NULL
LIMIT 1;