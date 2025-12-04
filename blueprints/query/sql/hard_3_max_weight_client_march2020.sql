SELECT c.*
FROM client c
JOIN (
  SELECT i.client_id, SUM(i.total_weight_kg) AS w
  FROM invoice i
  WHERE i.invoice_date >= '2020-03-01' AND i.invoice_date < '2020-04-01'
  GROUP BY i.client_id
  ORDER BY w DESC
  LIMIT 1
) t ON t.client_id=c.id;