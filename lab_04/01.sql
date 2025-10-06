-- Определяемую пользователем скалярную функцию CLR
CREATE OR REPLACE FUNCTION get_driver_full_name_py(driver_id_param INTEGER)
RETURNS TEXT
AS $$
    plan = plpy.prepare("SELECT first_name, last_name FROM Driver WHERE id = $1", ["integer"])
    result = plpy.execute(plan, [driver_id_param])
    if result:
        return result[0]["first_name"] + " " + result[0]["last_name"]
    else:
        return None
$$ LANGUAGE plpython3u;


SELECT get_driver_full_name_py(1);