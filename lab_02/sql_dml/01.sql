-- 1. Инструкция SELECT, использующая предикат сравнения. 
SELECT DISTINCT C1.brand, C1.model, C1.registration_plate, C2.registration_plate, C1.mileage, C2.mileage 
FROM Car C1 JOIN Car AS C2 ON C2.brand = C1.brand AND C2.model = C1.model 
WHERE C2.id <> C1.id AND C1.mileage < 10000 AND C2.mileage < 10000
 AND C1.registration_plate IS NOT NULL 
ORDER BY C1.brand, C1.model, C1.mileage DESC;
