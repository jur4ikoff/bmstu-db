-- 24. Оконные функции. Использование конструкций MIN/MAX/AVG OVER() 
SELECT 
    t.id AS trip_id,
    d.first_name || ' ' || d.last_name AS driver_name,
    t.price AS trip_price,
    t.score AS trip_score,
    AVG(t.price) OVER(PARTITION BY t.driver_id) AS avg_driver_price,
    MIN(t.price) OVER(PARTITION BY t.driver_id) AS min_driver_price,
    MAX(t.price) OVER(PARTITION BY t.driver_id) AS max_driver_price,
    AVG(t.score) OVER(PARTITION BY t.driver_id) AS avg_driver_rating,
	COUNT(t.score) OVER(PARTITION BY t.driver_id) AS count_driver_trips
FROM Trip t
LEFT JOIN Driver d ON t.driver_id = d.id
ORDER BY trip_id, driver_name, t.price DESC;