SELECT full_name, position, hired_at
FROM personal
WHERE hired_at >= (CURRENT_DATE - INTERVAL 10 DAY);