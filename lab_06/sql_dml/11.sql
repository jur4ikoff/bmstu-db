-- 11. Создание новой временной локальной таблицы из результирующего набора данных инструкции SELECT
-- Создание временной таблицы
CREATE TEMP TABLE DriverStats AS
SELECT 
    driver_id,
    COUNT(*) AS total_trips,
    SUM(price) AS total_earnings,
    AVG(score) AS avg_rating
FROM Trip
WHERE driver_id IS NOT NULL
GROUP BY driver_id;

-- Использование
SELECT * FROM DriverStats;