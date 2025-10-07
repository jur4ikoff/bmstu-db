-- Извлечь JSON фрагмент из JSON документа
SELECT profile->'vehicle' AS car_model
FROM driver_extended_info
WHERE driver_id = 1;