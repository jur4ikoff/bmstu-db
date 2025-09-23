-- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3
SELECT 'Наивысший пробег' AS criteria,
       brand || ' ' || model AS car_info,
       mileage
FROM Car
WHERE mileage = ( 
    SELECT MAX(car_mileage)
    FROM ( 
        SELECT mileage as car_mileage
        FROM Car
        WHERE mileage IS NOT NULL
    ) 
)
AND mileage IS NOT NULL;