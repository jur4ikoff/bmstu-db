-- Определяемая пользователем табличная функция
CREATE OR REPLACE FUNCTION find_suspicious_trips(
    threshold_percentile NUMERIC DEFAULT 95.0
)
RETURNS TABLE (
    trip_id INTEGER,
    driver_name TEXT,
    passenger_name TEXT,
    price INTEGER,
    score INTEGER,
    reason TEXT
)
AS $$
    import numpy as np

    # Получаем все поездки с именами
    plan = plpy.prepare("""
        SELECT 
            t.id AS trip_id,
            d.first_name || ' ' || d.last_name AS driver_name,
            p.first_name || ' ' || p.last_name AS passenger_name,
            t.price,
            t.score
        FROM Trip t
        JOIN Driver d ON t.driver_id = d.id
        JOIN Passenger p ON t.passenger_id = p.id
    """)
    
    results = plpy.execute(plan)

    if not results:
        return []

    prices = [row["price"] for row in results if row["price"] is not None]
    
    if prices:
        percentile_val = np.percentile(prices, threshold_percentile)
    else:
        percentile_val = 0

    output = []
    for row in results:
        reasons = []

        # Проверка на высокая цену
        if row["price"] is not None and row["price"] >= percentile_val and len(prices) > 1:
            reasons.append(f"high_price (>={int(percentile_val)})")

        # Проверка на низкий рейтинг
        if row["score"] is not None and row["score"] <= 2:
            reasons.append("low_rating")

        if reasons:
            output.append((
                row["trip_id"],
                row["driver_name"],
                row["passenger_name"],
                row["price"],
                row["score"],
                "; ".join(reasons)
            ))

    return output
$$ LANGUAGE plpython3u;

SELECT * FROM find_suspicious_trips(90.0);