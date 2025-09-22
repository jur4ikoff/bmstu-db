-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET
UPDATE Trip
SET score = (SELECT AVG(score) FROM Trip)
WHERE id = 20