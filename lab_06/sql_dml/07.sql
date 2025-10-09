-- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов
SELECT 
    brand,
    
    AVG(mileage) AS avg_mileage,
    SUM(mileage) / COUNT(id) AS calculated_avg_mileage,
    
    MAX(mileage) AS max_mileage,
    MIN(mileage) AS min_mileage,
    
    COUNT(*) AS car_count
    
FROM Car
WHERE mileage IS NOT NULL
GROUP BY brand
HAVING COUNT(mileage) > 1;