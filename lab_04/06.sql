CREATE OR REPLACE FUNCTION change_score()
RETURNS TRIGGER
AS $$
    driver_id = TD["new"]["driver_id"]

    plan = plpy.prepare("SELECT score FROM Trip WHERE driver_id = $1 AND score IS NOT NULL", ["integer"])
    result = plpy.execute(plan, [driver_id])
    
    if len(result) == 0:
        new_score = None
    else:
        scores = [row["score"] for row in result]
        new_score = sum(scores) / len(scores)
    
    update_plan = plpy.prepare("UPDATE Driver SET score = $1 WHERE id = $2", ["numeric", "integer"])
    plpy.execute(update_plan, [new_score, driver_id])
    
    return None
$$ LANGUAGE plpython3u;


DROP TRIGGER IF EXISTS trigger_suspicious_trip ON Trip;

CREATE TRIGGER trigger_change_score
    AFTER INSERT ON Trip
    FOR EACH ROW
    EXECUTE FUNCTION change_score();


-- SELECT setval('trip_id_seq', (SELECT MAX(id) FROM trip));
-- SELECT * FROM Trip

-- SELECT setval(pg_get_serial_sequence('car', 'id'), COALESCE(MAX(id), 0) + 1) FROM trip;

INSERT INTO Trip (driver_id, passenger_id, payment_id, source_address, destenation_address, price, score)
VALUES (1, 1, 1, 'A', 'B', 2000, 5);