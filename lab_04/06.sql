-- Определяемый пользователем тип данных
-- CREATE TYPE driver_name AS (
--     first_name TEXT,
--     last_name TEXT
-- );

CREATE OR REPLACE FUNCTION get_driver_name(driver_id_param INTEGER)
RETURNS driver_name
LANGUAGE plpython3u
AS $$
    plan = plpy.prepare("SELECT first_name, last_name FROM driver WHERE id = $1", ["integer"])
    result = plpy.execute(plan, [driver_id_param])
    
    if result:
        # Возвращаем словарь — PL/Python сопоставит его с типом driver_name
        return {
            "first_name": result[0]["first_name"],
            "last_name": result[0]["last_name"]
        }
    else:
        return None
$$;

-- Получить имя водителя с ID = 1
SELECT get_driver_name(1);