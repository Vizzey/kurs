SELECT p.full_name
FROM personal p
LEFT JOIN invoice i ON i.personal_id=p.id
WHERE i.id IS NULL
ORDER BY p.full_name;