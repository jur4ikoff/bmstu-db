-- Процедура
CREATE OR REPLACE PROCEDURE check_driver_issues()
LANGUAGE plpython3u
AS $func$
    # Получаем всех водителей с их данными и статистикой поездок
    query = """
        SELECT 
            d.id,
            d.first_name,
            d.last_name,
            d.experience,
            COUNT(t.id) AS trip_count,
            AVG(t.score) AS avg_score
        FROM Driver d
        LEFT JOIN Trip t ON d.id = t.driver_id AND t.score IS NOT NULL
        GROUP BY d.id, d.first_name, d.last_name, d.experience
    """
    drivers = plpy.execute(query)

    issue_found = False

    for drv in drivers:
        driver_id = drv["id"]
        name = f"{drv['first_name']} {drv['last_name']}"
        experience = drv["experience"] or 0
        trip_count = drv["trip_count"] or 0
        avg_score = drv["avg_score"]

        reasons = []

        if avg_score is not None and avg_score <= 3.0:
            reasons.append(f"low_avg_score ({avg_score:.2f})")

        if experience >= 5 and trip_count < 3:
            reasons.append("experienced_but_inactive")

        if trip_count == 0:
            reasons.append("no_trips")

        if reasons:
            issue_found = True
            plpy.warning(f"Driver issue: ID={driver_id}, Name='{name}', Reasons: {', '.join(reasons)}")

    if not issue_found:
        plpy.info("No driver issues detected.")
    else:
        plpy.info("Driver issue check completed. See warnings above.")
$func$;

CALL check_driver_issues();