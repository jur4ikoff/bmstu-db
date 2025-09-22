-- 2. Инструкция SELECT, использующая предикат BETWEEN. 
SELECT DISTINCT id, model, brand, vin_number registation_plate, mileage
FROM car
WHERE mileage BETWEEN 10000 AND 20000
