-- 22. Инструкция SELECT, использующая простое обобщенное табличное выражение
WITH DriverEarningsCTE (driver_id, total_earnings) AS (
    SELECT driver_id, SUM(price) AS earnings
    FROM Trip
    WHERE driver_id IS NOT NULL
    GROUP BY driver_id
)
SELECT 
    AVG(total_earnings) AS "Средний заработок водителя",
    SUM(total_earnings) AS "Общий заработок всех водителей",
    COUNT(*) AS "Количество водителей с поездками"
FROM DriverEarningsCTE;