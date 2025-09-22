-- 9. Инструкция SELECT, использующая простое выражение CASEx
SELECT 
    d.first_name,
    d.last_name,
    d.experience,
    t.score,
    CASE t.score
        WHEN 5 THEN 'Отлично'
        WHEN 4 THEN 'Хорошо'
        WHEN 3 THEN 'Нормально'
        WHEN 2 THEN 'Плохо'
        WHEN 1 THEN 'Ужасно'
        ELSE 'Нет оценки' 
    END AS trip_rating
FROM Driver d
JOIN Trip t ON d.id = t.driver_id
WHERE t.score IS NOT NULL;