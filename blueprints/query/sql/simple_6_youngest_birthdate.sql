SELECT full_name, birth_date
FROM personal
WHERE birth_date IS NOT NULL
ORDER BY birth_date DESC
LIMIT 1;