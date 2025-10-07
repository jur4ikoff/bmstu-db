-- Пользовательскую агрегатную функцию
-- Подсчет среднего, оценки входят только в диапазон [2, 5]
CREATE OR REPLACE FUNCTION filtered_avg_score(scores INTEGER[])
RETURNS NUMERIC
AS $$
    if not scores:
        return None

    # оставляем только >= 2
    filtered = [s for s in scores if s is not None and s >= 2]

    if not filtered:
        return None

    avg = sum(filtered) / len(filtered)
    return round(avg, 2)
$$ LANGUAGE plpython3u;

SELECT filtered_avg_score(
    ARRAY_AGG(score)
) AS reliable_avg_score
FROM Trip
-- WHERE driver_id = 1;
-- Либо для конкретного водителя, либо для всех