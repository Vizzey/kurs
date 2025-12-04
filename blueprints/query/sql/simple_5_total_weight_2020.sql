SELECT c.full_name, SUM(i.total_weight_kg) AS total_weight_kg
FROM client c
JOIN invoice i ON i.client_id=c.id
WHERE YEAR(i.invoice_date)=2020
GROUP BY c.id
ORDER BY total_weight_kg DESC;