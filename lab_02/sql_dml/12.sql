-- 12. Инструкция SELECT, использующая вложенные коррелированные подзапросы
-- в качестве производных таблиц в предложении FROM

SELECT 'By trip count' AS Criteria, 
       d.first_name || ' ' || d.last_name AS "Best Driver"
FROM Driver d 
JOIN (
    SELECT driver_id, COUNT(*) AS trip_count
    FROM Trip
    GROUP BY driver_id
    ORDER BY trip_count DESC
    LIMIT 10
) AS TopDriver ON TopDriver.driver_id = d.id;