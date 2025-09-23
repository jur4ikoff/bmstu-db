-- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом. 
SELECT driver_id, passenger_id, payment_id, source_address, destenation_address, price, score
FROM trip
WHERE driver_id IN (SELECT id
FROM Driver
WHERE first_name = 'Christine')
