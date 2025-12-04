CREATE OR REPLACE VIEW v_client_counts_2020 AS
SELECT client_id, COUNT(*) AS trips
FROM invoice
WHERE YEAR(invoice_date)=2020
GROUP BY client_id;

SELECT c.*, v.trips
FROM v_client_counts_2020 v
JOIN client c ON c.id=v.client_id
ORDER BY v.trips DESC
LIMIT 1;