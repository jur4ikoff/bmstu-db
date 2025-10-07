-- Извлечь JSON фрагмент из JSON документа
SELECT profile->'vehicle'->>'model' AS car_model
FROM driver_extended_info
WHERE driver_id = 1;