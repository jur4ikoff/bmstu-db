-- 6. Инструкция SELECT, использующая предикат сравнения с квантором. 
SELECT *
FROM Trip
WHERE price > ALL (SELECT price
				FROM Trip
				WHERE score < 3)

ORDER BY price