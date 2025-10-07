SELECT json_agg(t) AS drivers
FROM (
    SELECT id, first_name, last_name, experience, score, date_of_birthday, address
    FROM driver
) t;