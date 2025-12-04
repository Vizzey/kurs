SELECT plate_no
FROM vehicle
WHERE plate_no LIKE CONCAT('%%', %(series)s, '%%');