-- Таблица владельцев
CREATE TABLE Owner (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20)
);

-- Таблица животных
CREATE TABLE Animal (
    id INT PRIMARY KEY AUTO_INCREMENT,
    species VARCHAR(100) NOT NULL,
    breed VARCHAR(100),
    nickname VARCHAR(50) UNIQUE  -- Замена chip_number на nickname
);

-- Таблица болезней
CREATE TABLE Disease (
    id INT PRIMARY KEY AUTO_INCREMENT,
    disease_name VARCHAR(255) NOT NULL,
    symptom TEXT,
    analysis TEXT
);

-- Промежуточная таблица: связь многие-ко-многим Animal — Owner
CREATE TABLE AnimalOwner (
    animal_id INT NOT NULL,
    owner_id INT NOT NULL,
    acquisition_date DATE,  -- дата, когда владелец получил животное (опционально)
    PRIMARY KEY (animal_id, owner_id)
);

-- Промежуточная таблица: связь многие-ко-многим Animal — Disease
CREATE TABLE AnimalDisease (
    animal_id INT NOT NULL,
    disease_id INT NOT NULL,
    diagnosis_date DATE,
    PRIMARY KEY (animal_id, disease_id)
);

-- Добавление внешних ключей через ALTER TABLE

-- Для AnimalOwner
ALTER TABLE AnimalOwner
ADD CONSTRAINT fk_animalowner_animal
FOREIGN KEY (animal_id) REFERENCES Animal(id) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_animalowner_owner
FOREIGN KEY (owner_id) REFERENCES Owner(id) ON DELETE CASCADE ON UPDATE CASCADE;

-- Для AnimalDisease
ALTER TABLE AnimalDisease
ADD CONSTRAINT fk_animaldisease_animal
FOREIGN KEY (animal_id) REFERENCES Animal(id) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_animaldisease_disease
FOREIGN KEY (disease_id) REFERENCES Disease(id) ON DELETE CASCADE ON UPDATE CASCADE;