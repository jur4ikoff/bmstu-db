SELECT p.id, p.first_name, p.last_name
FROM Passenger p
JOIN Trip t ON t.passenger_id = p.id
GROUP BY p.id
HAVING COUNT(DISTINCT t.driver_id) = 1
AND COUNT(t.id) > 1;