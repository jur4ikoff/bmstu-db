-- Определяемая пользователем скалярную функцию 
-- Оценка надежности водителя
CREATE OR REPLACE FUNCTION driver_reliability_score(driver_id_param INTEGER)
RETURNS NUMERIC
AS $$
    from datetime import date

    # Получаем основные данные о водителе и его машине
    driver_plan = plpy.prepare("""
        SELECT 
            d.experience,
            d.date_of_birthday,
            c.mileage
        FROM Driver d
        LEFT JOIN Car c ON d.car_id = c.id
        WHERE d.id = $1
    """, ["integer"])
    
    driver_result = plpy.execute(driver_plan, [driver_id_param])
    
    # Если водителя нет — возвращаем NULL
    if not driver_result:
        return None

    drv = driver_result[0]
    experience = drv["experience"] or 0
    dob_str = drv["date_of_birthday"]  # в формате 'YYYY-MM-DD'
    mileage = drv["mileage"] or 0

    # Считаем возраст
    try:
        dob = date.fromisoformat(dob_str)
        today = date.today()
        age = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1
    except Exception:
        age = 30  # значение по умолчанию при ошибке

    # Шаг 3: Получаем средний рейтинг поездок водителя
    trip_plan = plpy.prepare("""
        SELECT AVG(score) AS avg_score, COUNT(*) AS trip_count
        FROM Trip
        WHERE driver_id = $1 AND score IS NOT NULL
    """, ["integer"])
    
    trip_result = plpy.execute(trip_plan, [driver_id_param])
    avg_score = trip_result[0]["avg_score"] or 0.0
    trip_count = trip_result[0]["trip_count"] or 0

    # Если нет поездок — используем рейтинг из профиля (Driver.score)
    if trip_count == 0:
        profile_plan = plpy.prepare("SELECT score FROM Driver WHERE id = $1", ["integer"])
        profile_result = plpy.execute(profile_plan, [driver_id_param])
        avg_score = profile_result[0]["score"] if profile_result and profile_result[0]["score"] is not None else 5.0

    # Начинаем с базового балла
    score = 50.0

    # Добавляем бонусы и штрафы
    # Бонус за стаж (макс. +20)
    score += min(experience * 2, 20)

    # Бонус за возраст
    if 25 <= age <= 60:
        score += 10
    elif age < 21:
        score -= 15  # слишком молод
    elif age > 70:
        score -= 10  # возрастной риск

    # Бонус за хороший рейтинг
    if avg_score >= 4.5:
        score += 10
    elif avg_score >= 4.0:
        score += 5
    elif avg_score < 3.5:
        score -= 10

    # Штраф за изношенную машину
    if mileage > 300000:
        score -= 8
    elif mileage > 200000:
        score -= 4

    # Ограничиваем диапазон [0, 100]
    score = max(0.0, min(100.0, score))

    return round(score, 1)
$$ LANGUAGE plpython3u;

SELECT driver_reliability_score(1) AS reliability;

-- Использовать в отчёте
SELECT 
    d.id,
    d.first_name,
    d.last_name,
    driver_reliability_score(d.id) AS reliability_score
FROM Driver d
ORDER BY reliability_score DESC;