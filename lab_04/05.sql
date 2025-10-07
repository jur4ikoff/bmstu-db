CREATE OR REPLACE FUNCTION log_suspicious_trip()
RETURNS TRIGGER
LANGUAGE plpython3u
AS $func$
    import numpy as np

    result = plpy.execute("SELECT price FROM Trip WHERE price IS NOT NULL")
    prices = [row["price"] for row in result if row["price"] is not None]

    if len(prices) < 5:
        return None

    new_price = TD["new"]["price"]
    if new_price is None or new_price <= 0:
        return None

    mean_price = np.mean(prices)
    std_price = np.std(prices)
    # стандартное отклонение
    threshold = mean_price + 2 * std_price

    if new_price > threshold:
        driver_id = TD["new"]["driver_id"]
        passenger_id = TD["new"]["passenger_id"]
        plpy.warning(
            f"Suspicious trip detected! "
            f"Trip price: {new_price}, "
            f"Threshold: {threshold:.2f}, "
            f"Driver ID: {driver_id}, "
            f"Passenger ID: {passenger_id}"
        )

    return None  # AFTER-триггер всегда возвращает None
$func$;


DROP TRIGGER IF EXISTS trigger_suspicious_trip ON Trip;

CREATE TRIGGER trigger_suspicious_trip
    AFTER INSERT ON Trip
    FOR EACH ROW
    EXECUTE FUNCTION log_suspicious_trip();


-- SELECT setval('trip_id_seq', (SELECT MAX(id) FROM trip));
-- SELECT * FROM Trip

-- SELECT setval(pg_get_serial_sequence('car', 'id'), COALESCE(MAX(id), 0) + 1) FROM trip;

INSERT INTO Trip (driver_id, passenger_id, payment_id, source_address, destenation_address, price, score)
VALUES (1, 1, 1, 'A', 'B', 2000, 5);