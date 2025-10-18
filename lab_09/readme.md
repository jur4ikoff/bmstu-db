# Условие
УЖАС

-- SELECT setval(pg_get_serial_sequence('Passenger', 'id'), coalesce(max(id), 0) + 1, false)
-- FROM Passenger;