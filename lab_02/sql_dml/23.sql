-- 23. Инструкция SELECT, использующая рекурсивное обобщенное табличное выражение
-- Весто 

WITH RECURSIVE SimpleHierarchy AS (
	-- Первый человек становится закрепленным элементом
    SELECT 
        id,
        first_name,
        last_name,
        NULL::INTEGER AS manager_id,
        0 AS level
    FROM Driver
    WHERE id = 1
    
    UNION ALL   
    SELECT 
        d.id,
        d.first_name,
        d.last_name,
        sh.id AS manager_id,
        sh.level + 1 AS level
    FROM Driver d
    JOIN SimpleHierarchy sh ON d.id = sh.id + 1 -- Возьми водителя, чей id на 1 больше предыдущего
    WHERE d.id <= (SELECT MAX(id) FROM Driver)  -- останавливаемся на максимальном ID
)

-- Запрос для вывода данных из таблицы
SELECT 
    level AS "Уровень",
    id AS "ID водителя",
    first_name || ' ' || last_name AS "Водитель",
    manager_id AS "ID менеджера"
FROM SimpleHierarchy
ORDER BY id;