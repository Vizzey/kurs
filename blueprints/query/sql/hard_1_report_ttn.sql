SELECT i.id AS ttn_no,
       p.full_name AS employee,
       i.invoice_date,
       i.total_weight_kg
FROM invoice i
JOIN personal p ON p.id=i.personal_id
ORDER BY i.invoice_date, i.id;