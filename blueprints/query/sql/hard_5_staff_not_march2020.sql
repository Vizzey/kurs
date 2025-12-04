SELECT p.full_name
FROM personal p
LEFT JOIN (
  SELECT DISTINCT personal_id
  FROM invoice
  WHERE invoice_date >= '2020-03-01' AND invoice_date < '2020-04-01'
) m ON m.personal_id=p.id
WHERE m.personal_id IS NULL
ORDER BY p.full_name;