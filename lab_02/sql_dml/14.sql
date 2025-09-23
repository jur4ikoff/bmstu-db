-- 14. Инструкция SELECT, консолидирующая данные с помощью предложения
-- GROUP BY, но без предложения HAVING.
SELECT
	d.id,
	d.first_name,
	d.last_name,
	d.experience,
	COUNT (t.id) as total_trips,
	MIN (t.price) AS min_price,
	MAX (t.price) AS max_price
	
FROM Driver d
LEFT OUTER JOIN Trip t ON t.driver_id = d.id
GROUP BY d.id
ORDER BY total_trips DESC