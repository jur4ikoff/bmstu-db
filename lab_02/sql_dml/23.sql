-- Доделать
WITH RECURSIVE SimpleHierarchy AS (
    -- Начинаем с первого водителя
    SELECT 
        id,
        first_name,
        last_name,
        NULL::INTEGER AS manager_id,
        0 AS level
    FROM Driver
    WHERE id = 1
    
    UNION ALL
    
    -- Каждый следующий водитель подчиняется предыдущему
    SELECT 
        d.id,
        d.first_name,
        d.last_name,
        sh.id AS manager_id,
        sh.level + 1 AS level
    FROM Driver d
    INNER JOIN SimpleHierarchy sh ON d.id = sh.id + 1
    WHERE d.id <= (SELECT MAX(id) FROM Driver)  -- останавливаемся на максимальном ID
)
SELECT 
    level AS "Уровень",
    id AS "ID водителя",
    first_name || ' ' || last_name AS "Водитель",
    manager_id AS "ID менеджера"
FROM SimpleHierarchy
ORDER BY id;