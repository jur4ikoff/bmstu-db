-- 6. Инструкция SELECT, использующая предикат сравнения с квантором
-- Получить записи, где цена выше чем все цены за поездки, где рейтинг ниже 3
SELECT *
FROM Trip
WHERE price > ALL (SELECT price
				FROM Trip
				WHERE score < 3)

ORDER BY price