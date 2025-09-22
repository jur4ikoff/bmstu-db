-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в предложении WHERE
-- Удаление машин, которые не используются
DELETE FROM Car
WHERE id IN ( 
    SELECT c.id
    FROM Car c LEFT OUTER JOIN Driver d ON c.id = d.car_id
    WHERE d.car_id IS NULL
);