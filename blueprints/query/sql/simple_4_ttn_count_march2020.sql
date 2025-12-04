SELECT COUNT(*) AS ttn_count
FROM invoice
WHERE invoice_date >= '2020-03-01' AND invoice_date < '2020-04-01';