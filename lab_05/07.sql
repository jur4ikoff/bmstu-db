-- Обновить инфомацию
UPDATE driver_extended_info
SET profile = jsonb_set(profile, '{personal,phone}', '"+79123456789"')
WHERE driver_id = 123;