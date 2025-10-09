-- 8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов
SELECT 
	t.price,
    (SELECT AVG(price) FROM Trip) AS avg_price_all_trips,
    (SELECT MAX(price) FROM Trip WHERE driver_id = t.driver_id) AS max_price_this_driver,
    t.price - (SELECT AVG(price) FROM Trip) AS difference_from_avg
FROM Trip t;