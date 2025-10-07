-- Извлечь значения конкретных узлов или атрибутов JSON документа
SELECT driver_id, profile->'personal'->>'full_name' AS full_name
FROM driver_extended_info;