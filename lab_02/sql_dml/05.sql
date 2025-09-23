-- 5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом
-- Находит машины, не разу не задействоваванные в поездках

SELECT c.id, c.brand, c.model, c.registration_plate, c.vin_number
FROM Car c
WHERE EXISTS (
    SELECT c2.id
    FROM Car c2

    LEFT OUTER JOIN Driver d ON c2.id = d.car_id 
    LEFT OUTER JOIN Trip t ON d.id = t.driver_id
    WHERE t.driver_id IS NULL 
      AND c2.id = c.id
);