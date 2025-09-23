-- 3. Инструкция SELECT, использующая предикат LIKE. 
Select first_name, last_name, date_of_birthday, address
FROM passenger
WHERE address LIKE '%Park%'