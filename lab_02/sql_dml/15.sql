-- Инструкция SELECT, консолидирующая данные с помощью
-- предложения GROUP BY и предложения HAVING

SELECT 
    d.id,
    d.first_name,
    d.last_name,
    AVG(t.price) AS avg_earnings_per_trip,
    (SELECT AVG(price) FROM Trip) AS overall_avg_earnings
FROM Driver d 
JOIN Trip t ON t.driver_id = d.id
GROUP BY d.id, d.first_name, d.last_name
HAVING AVG(t.price) > (SELECT AVG(price) FROM Trip)
ORDER BY avg_earnings_per_trip DESC;