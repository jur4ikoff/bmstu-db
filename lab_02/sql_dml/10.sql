-- 10. Инструкция SELECT, использующая поисковое выражение CASE
SELECT 
	d.first_name, d.last_name, d.experience,
	CASE
		WHEN d.experience >= 40 THEN 'Старичок'
        WHEN d.experience > 10 THEN 'Опытный'
        WHEN d.experience < 10 THEN 'Молодой'
		WHEN d.experience < 1 THEN 'Новичок'
      	ELSE 'Без опыта'
	END AS EXP
FROM Driver d;