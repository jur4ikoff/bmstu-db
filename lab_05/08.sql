-- Разделить поле

SELECT jsonb_array_elements(profile->'vehicle'->'features') AS feature
FROM driver_extended_info
WHERE driver_id = 1;
