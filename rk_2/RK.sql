

-----------------------------
------- Задание 1 -----------
-----------------------------

-- Таблица владельцев
CREATE TABLE Owner (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20)
);

-- Таблица животных
CREATE TABLE Animal (
    id SERIAL PRIMARY KEY,
    species VARCHAR(100) NOT NULL,
    breed VARCHAR(100),
    nickname VARCHAR(50) UNIQUE
);

-- Таблица болезней
CREATE TABLE Disease (
    id SERIAL PRIMARY KEY,
    disease_name VARCHAR(255) NOT NULL,
    symptom TEXT,
    analysis TEXT
);

-- Промежуточная таблица: связь многие-ко-многим Animal — Owner
CREATE TABLE AnimalOwner (
    animal_id INT NOT NULL,
    owner_id INT NOT NULL,
    acquisition_date DATE,
    PRIMARY KEY (animal_id, owner_id)
);

-- Промежуточная таблица: связь многие-ко-многим Animal — Disease
CREATE TABLE AnimalDisease (
    animal_id INT NOT NULL,
    disease_id INT NOT NULL,
    diagnosis_date DATE,
    PRIMARY KEY (animal_id, disease_id)
);


-- Владельцы
INSERT INTO Owner (full_name, address, phone) VALUES
('Иван Иванов', 'ул. Ленина, д. 1', '+79123456789'),
('Мария Петрова', 'пр. Мира, д. 5', '+79234567890'),
('Алексей Сидоров', 'ул. Гагарина, д. 12', '+79345678901'),
('Елена Козлова', 'пер. Цветной, д. 3', '+79456789012'),
('Дмитрий Волков', 'ул. Пушкина, д. 8', '+79567890123'),
('Ольга Морозова', 'ул. Чехова, д. 22', '+79678901234'),
('Сергей Николаев', 'пр. Победы, д. 15', '+79789012345'),
('Анна Терехова', 'ул. Свободы, д. 7', '+79890123456'),
('Николай Федоров', 'ул. Советская, д. 10', '+79901234567'),
('Татьяна Широкова', 'ул. Комсомольская, д. 4', '+79012345678');

-- Животные
INSERT INTO Animal (species, breed, nickname) VALUES
('Собака', 'Лабрадор', 'Барон'),
('Хомяк', 'Персидский', 'Умка'),
('Собака', 'Пудель', 'Шарик'),
('Кошка', 'Персидская', 'Снежок'),
('Собака', 'Хаски', 'Ветер'),
('Кошка', 'Британская', 'Том'),
('Собака', 'Терьер', 'Рекс'),
('Кошка', 'Мейн-кун', 'Гром'),
('Собака', 'Доберман', 'Цезарь'),
('Кошка', 'Шотландская', 'Леди');

-- Болезни
INSERT INTO Disease (disease_name, symptom, analysis) VALUES
('Болезнь 0', 'Высокая температура, рвота', 'Анализ крови'),
('Болезнь 1', 'Потеря аппетита', 'Биохимический анализ'),
('Болезнь 2', 'Тошнота', '7 дней подождать'),
('Бешенство', 'Агрессия, слюноотделение', 'Бог поможет'),
('Болезнь легких', 'Чихание, сопли', 'ПЦР-анализ'),
('Болезнь кожи', 'Выпадение шерсти, зуд', 'Анализ кожи'),
('Отит', 'Боль в ушах', 'Посмотреть что там с ним'),
('Конъюнктивит', 'Покраснение глаз', 'Осмотр офтальмолога'),
('Панкреатит', 'Острая боль в животе', 'УЗИ');

-- Связь животных с владельцами
INSERT INTO AnimalOwner (animal_id, owner_id, acquisition_date) VALUES
(1, 1, '2020-01-10'),
(2, 2, '2019-02-15'),
(3, 3, '2024-03-20'),
(4, 4, '2003-04-05'),
(5, 5, '2023-05-12'),
(6, 6, '2025-06-18'),
(8, 8, '2023-07-30'),
(10, 10, '2025-09-01'),
(1, 2, '2015-09-13'),
(6, 4, '2025-10-23'), 
(2, 4, '2020-01-05'); 

-- Связь животных с болезнями
INSERT INTO AnimalDisease (animal_id, disease_id, diagnosis_date) VALUES
(1, 1, '2025-03-10'),
(2, 2, '2025-04-05'),
(3, 3, '2025-05-12'),
(4, 4, '2025-06-01'),
(5, 5, '2025-07-20'),
(8, 8, '2025-08-11'),
(9, 9, '2025-09-02'),
(10, 1, '2025-10-18'), -- Бедный кот
(10, 2, '2025-10-19'),
(10, 3, '2025-10-19'),
(10, 10, '2025-10-19');


-----------------------------
------ Задание 2 ------------
-----------------------------

-- Запрос 1: оконная функция
SELECT
    a.nickname AS animal_nickname,
    a.species,
    a.breed,
    o.full_name AS owner_name,
    ad.diagnosis_date,
    ROW_NUMBER() OVER (
        PARTITION BY o.id
        ORDER BY ad.diagnosis_date ASC
    ) AS visit_number  -- Номер визита владельца (по всем его животным)
FROM Animal a
JOIN AnimalOwner ao ON a.id = ao.animal_id
JOIN Owner o ON ao.owner_id = o.id
JOIN AnimalDisease ad ON a.id = ad.animal_id
ORDER BY o.full_name, ad.diagnosis_date;

-- 2 запрос
-- GROUP BY, HAVING
-- Функция находит владельцев, у которых количество животных больше 2
SELECT COUNT(*), id, full_name, address FROM Owner o
JOIN AnimalOwner ao ON ao.owner_id = o.id
GROUP BY owner_id, id
HAVING COUNT(*) >= 2

-- 3 запрос
-- Скалярные подзапросы
-- Выводит инфу по животному + количество болезней
SELECT
	id, species, breed, nickname,
	(SELECT COUNT(*) FROM AnimalDisease ad WHERE ad.animal_id = id) as disease_count
FROM Animal a
ORDER BY disease_count ASC, id


-----------------------------
-------- Задание 3 ----------
-----------------------------

DROP PROCEDURE IF EXISTS DropAllIndexesForTable(TEXT, TEXT);
CREATE OR REPLACE PROCEDURE DropAllIndexesForTable(
    target_schema TEXT,
    target_table TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    idx RECORD;
    idx_name TEXT;
    tbl_oid OID;
BEGIN
    -- Проверка на то, сществует ли таблица в схеме
    SELECT c.oid INTO tbl_oid
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relname = target_table
      AND n.nspname = target_schema
      AND c.relkind = 'r';

    IF tbl_oid IS NULL THEN
        RAISE EXCEPTION 'Table %.% does not exist', target_schema, target_table;
    END IF;

    -- Цикл по всем индексам таблицы, кроме первичного ключа
    FOR idx IN
        SELECT
            i.indexrelid::regclass AS index_name,
            i.indisprimary
        FROM pg_index i
        WHERE i.indrelid = tbl_oid
          AND NOT i.indisprimary
    LOOP
        idx_name := idx.index_name::TEXT;
        RAISE NOTICE 'Dropping index: %', idx_name;
        EXECUTE 'DROP INDEX ' || idx_name;
    END LOOP;

    RAISE NOTICE 'All non-primary indexes on table %.% have been dropped.', target_schema, target_table;
END;
$$;

-- Тестовая таблица
CREATE TABLE IF NOT EXISTS test_animals (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(50) NOT NULL,
    species VARCHAR(30)
);

-- Тестовые данные
INSERT INTO test_animals (nickname, species) VALUES
('Барон', 'Собака'),
('Мурка', 'Кошка'),
('Шарик', 'Собака');

-- Дополнительные индексы
CREATE INDEX idx_test_nickname ON test_animals (nickname);
CREATE INDEX idx_test_species ON test_animals (species);
CREATE UNIQUE INDEX idx_test_nickname_unique ON test_animals (nickname);

-- Вывод всех индексов 
SELECT indexname
FROM pg_indexes
WHERE tablename = 'test_animals'
  AND schemaname = 'public';

-- Вызов функции
CALL DropAllIndexesForTable('public', 'test_animals');