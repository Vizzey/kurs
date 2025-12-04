SELECT DISTINCT p.full_name
FROM invoice i
JOIN personal p ON p.id=i.personal_id
JOIN client c ON c.id=i.client_id
WHERE c.contract_no = %(contract)s
  AND i.invoice_date >= '2020-03-01' AND i.invoice_date < '2020-04-01'
ORDER BY p.full_name;