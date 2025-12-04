SELECT id, name, price, category
FROM product
WHERE (%(name)s IS NULL OR name LIKE %(name)s)
  AND price BETWEEN %(min_price)s AND %(max_price)s
ORDER BY price ASC
LIMIT 100;