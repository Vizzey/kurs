DROP DATABASE IF EXISTS vehicles;
CREATE DATABASE vehicles CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE vehicles;

CREATE TABLE client (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  phone VARCHAR(32),
  email VARCHAR(255),
  city VARCHAR(100),
  address VARCHAR(255),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  contract_no VARCHAR(32),
  total_weight_kg DECIMAL(14,3) NOT NULL DEFAULT 0.000
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE personal (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  position VARCHAR(100),
  phone VARCHAR(32),
  email VARCHAR(255),
  hired_at DATE,
  salary DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  birth_date DATE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE product (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(100),
  price DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  weight_kg DECIMAL(10,3) NOT NULL DEFAULT 0.000
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE vehicle (
  id INT AUTO_INCREMENT PRIMARY KEY,
  plate_no VARCHAR(20) NOT NULL UNIQUE,
  model VARCHAR(100),
  capacity_kg INT NOT NULL DEFAULT 0,
  is_active TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE invoice (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  personal_id INT NOT NULL,
  vehicle_id INT NULL,
  invoice_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(20) NOT NULL DEFAULT 'новый',
  total DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  total_weight_kg DECIMAL(12,3) NOT NULL DEFAULT 0.000,
  CONSTRAINT fk_invoice_client FOREIGN KEY (client_id) REFERENCES client(id),
  CONSTRAINT fk_invoice_personal FOREIGN KEY (personal_id) REFERENCES personal(id),
  CONSTRAINT fk_invoice_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicle(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE invoice_list (
  id INT AUTO_INCREMENT PRIMARY KEY,
  invoice_id INT NOT NULL,
  product_id INT NOT NULL,
  qty INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  line_total DECIMAL(12,2) NOT NULL,
  CONSTRAINT fk_invoicelist_invoice FOREIGN KEY (invoice_id) REFERENCES invoice(id),
  CONSTRAINT fk_invoicelist_product FOREIGN KEY (product_id) REFERENCES product(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO client (full_name, phone, email, city, address, created_at, contract_no) VALUES
('Иван Петров', '+995-555-0001', 'ivan.petrov@example.com', 'Тбилиси', 'ул. Руставели, 1', '2020-02-20 10:00:00', 'C-1001'),
('Анна Иванова', '+995-555-0002', 'anna.ivanova@example.com', 'Батуми', 'пр. Чавчавадзе, 10', '2020-02-25 11:00:00', 'C-1002'),
('Павел Соколов', '+995-555-0003', 'pavel.sokolov@example.com', 'Кутаиси', 'ул. Царя Тамары, 5', '2020-03-01 12:00:00', 'C-1003'),
('Ольга Смирнова', '+995-555-0004', 'olga.smirnova@example.com', 'Тбилиси', 'пр. Агмашенебели, 25', '2020-03-05 09:30:00', 'C-1004'),
('Сергей Волков', '+995-555-0005', 'sergey.volkov@example.com', 'Батуми', 'ул. Горгиладзе, 7', '2020-03-07 14:15:00', 'C-1005');

INSERT INTO personal (full_name, position, phone, email, hired_at, salary, birth_date) VALUES
('Марина Петрова', 'Менеджер по закупкам', '+995-555-0101', 'marina.p@example.com', '2020-03-10', 2000.00, '1992-04-10'),
('Никита Орлов', 'Продавец-консультант', '+995-555-0102', 'nikita.o@example.com', '2020-03-25', 1500.00, '1998-07-21'),
('Дарья Кузнецова', 'Администратор склада', '+995-555-0103', 'daria.k@example.com', '2019-08-20', 2200.00, '1990-12-05'),
('Роман Егоров', 'Логист', '+995-555-0104', 'roman.e@example.com', '2019-05-12', 1800.00, '1995-03-14'),
('Ирина Соколова', 'Бухгалтер', '+995-555-0105', 'irina.s@example.com', '2020-02-28', 2500.00, '1999-09-30');

INSERT INTO product (name, category, price, stock, weight_kg) VALUES
('Аккумулятор 60Ач', 'Электрика', 85.00, 40, 16.000),
('Масляный фильтр', 'Двигатель', 12.50, 150, 0.250),
('Тормозные колодки', 'Тормозная система', 45.00, 80, 2.200),
('Свеча зажигания', 'Двигатель', 8.90, 200, 0.080),
('Воздушный фильтр', 'Фильтры', 14.30, 100, 0.350);

INSERT INTO vehicle (plate_no, model, capacity_kg, is_active) VALUES
('AA-001-AA', 'Форд Транзит', 1500, 1),
('AA-002-AA', 'Мерседес Спринтер', 2000, 1),
('AA-003-AA', 'Рено Мастер', 1600, 1),
('AA-004-AA', 'Фольксваген Крафтер', 1700, 0),
('AA-005-AA', 'Ивеко Дэйли', 1800, 1);

INSERT INTO invoice (client_id, personal_id, vehicle_id, invoice_date, status, total, total_weight_kg) VALUES
(1, 3, 1, '2020-03-10 10:10:00', 'оплачен', 0.00, 0.000),
(2, 2, 2, '2020-03-12 11:20:00', 'оплачен', 0.00, 0.000),
(3, 1, NULL, '2020-03-20 09:00:00', 'новый', 0.00, 0.000),
(4, 5, 3, '2020-03-25 13:45:00', 'оплачен', 0.00, 0.000),
(5, 4, NULL, '2020-04-02 16:05:00', 'новый', 0.00, 0.000);

INSERT INTO invoice_list (invoice_id, product_id, qty, price, line_total) VALUES
(1, 1, 1, 85.00, 85.00),
(1, 2, 3, 12.50, 37.50),
(2, 3, 2, 45.00, 90.00),
(3, 4, 4, 8.90, 35.60),
(4, 5, 2, 14.30, 28.60);

UPDATE invoice i
JOIN (
  SELECT il.invoice_id, SUM(il.line_total) AS s
  FROM invoice_list il
  GROUP BY il.invoice_id
) t ON t.invoice_id=i.id
SET i.total=t.s;

UPDATE invoice i
JOIN (
  SELECT il.invoice_id, SUM(il.qty * p.weight_kg) AS w
  FROM invoice_list il
  JOIN product p ON p.id=il.product_id
  GROUP BY il.invoice_id
) t ON t.invoice_id=i.id
SET i.total_weight_kg=t.w;

UPDATE client c
JOIN (
  SELECT i.client_id, SUM(i.total_weight_kg) AS w
  FROM invoice i
  GROUP BY i.client_id
) s ON s.client_id=c.id
SET c.total_weight_kg=s.w;

DELIMITER //
CREATE PROCEDURE sp_recalc_totals_for_date(IN p_date DATE)
BEGIN
  UPDATE invoice i
  JOIN (
    SELECT il.invoice_id, SUM(il.qty*p.weight_kg) AS w, SUM(il.line_total) AS s
    FROM invoice_list il
    JOIN product p ON p.id=il.product_id
    JOIN invoice ix ON ix.id=il.invoice_id
    WHERE DATE(ix.invoice_date)=p_date
    GROUP BY il.invoice_id
  ) t ON t.invoice_id=i.id
  SET i.total_weight_kg=t.w, i.total=t.s
  WHERE DATE(i.invoice_date)=p_date;

  UPDATE client c
  JOIN (
    SELECT i.client_id, SUM(i.total_weight_kg) AS w
    FROM invoice i
    GROUP BY i.client_id
  ) s ON s.client_id=c.id
  SET c.total_weight_kg=s.w;
END//
CREATE TRIGGER trg_invoice_weight_update
AFTER UPDATE ON invoice
FOR EACH ROW
BEGIN
  IF NEW.total_weight_kg <> OLD.total_weight_kg THEN
    UPDATE client
    SET total_weight_kg = (
      SELECT IFNULL(SUM(total_weight_kg),0)
      FROM invoice
      WHERE client_id = NEW.client_id
    )
    WHERE id = NEW.client_id;
  END IF;
END//
DELIMITER ;
