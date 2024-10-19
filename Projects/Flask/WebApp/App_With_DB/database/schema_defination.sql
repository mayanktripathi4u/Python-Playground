create database if not exists `money_control`;

use `money_control`;

CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY auto_increment,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(200) NOT NULL,
  password VARCHAR(200) NOT NULL
);

-- drop table category;

CREATE TABLE IF NOT EXISTS category (
  id INT PRIMARY KEY auto_increment,
  category VARCHAR(100) NOT NULL,
  is_active VARCHAR(10) NOT NULL DEFAULT 'ACTV',
  create_by VARCHAR(100) NOT NULL,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_update_date DATETIME ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subcategory (
  id INT PRIMARY KEY auto_increment,
  category_id INT NOT NULL,
  subcategory VARCHAR(100) NOT NULL,
  is_active VARCHAR(10) NOT NULL DEFAULT 'ACTV',
  create_by VARCHAR(100) NOT NULL,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_update_date DATETIME ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_category_id
  FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS product (
  id INT PRIMARY KEY auto_increment,
  subcategory_id INT NOT NULL,
  product VARCHAR(100) NOT NULL,
  is_active VARCHAR(10) NOT NULL DEFAULT 'ACTV',
  create_by VARCHAR(100) NOT NULL,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_update_date DATETIME ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_subcategory_id
  FOREIGN KEY (subcategory_id) REFERENCES subcategory(id)
);

-- SELECT * FROM users LIMIT 5;

INSERT INTO category (category, create_by)
	SELECT 'Grocery', 'Mayank';
    
INSERT INTO subcategory (category_id, subcategory, create_by)
	SELECT 1, 'Vegetables', 'Mayank';
    
INSERT INTO product (subcategory_id, product, create_by)
	SELECT 1, 'Carrot', 'Mayank';


CREATE TABLE IF NOT EXISTS payment_mode (
  id INT PRIMARY KEY auto_increment,
  pay_mode VARCHAR(100) NOT NULL,
  card_nbr VARCHAR(100),
  card_expiration DATETIME,
  is_active VARCHAR(10) NOT NULL DEFAULT 'ACTV',
  create_by VARCHAR(100) NOT NULL,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_update_date DATETIME ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO payment_mode (pay_mode, card_nbr, card_expiration, create_by)
	SELECT 'Cash', NULL, NULL, 'Mayank' UNION
  SELECT 'BOA-CC', 'xxx-1234', '2026-01-03', 'Mayank' UNION
  SELECT 'BOA-DC', 'xxx-2345', '2026-01-03', 'Mayank' UNION
  SELECT 'Discover-CC', 'xxx-6758', '2026-01-03', 'Mayank' UNION
  SELECT 'CITI-CC', 'xxx-9874', '2026-01-03', 'Mayank' UNION
  SELECT 'Symphony-CC', 'xxx-0984', '2026-01-03', 'Mayank' UNION
  SELECT 'GiftCard-Walmart', 'xxx-ABC', '2026-01-03', 'Mayank' 
  ;

CREATE TABLE IF NOT EXISTS expense (
  id INT PRIMARY KEY auto_increment,
  purchase_from VARCHAR(100) NOT NULL,
  purchase_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_amount FLOAT NOT NULL DEFAULT 0.00,
  short_desc VARCHAR(200),
  is_active VARCHAR(10) NOT NULL DEFAULT 'ACTV',
  create_by VARCHAR(100) NOT NULL,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_update_date DATETIME ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS expense_details (
  id INT PRIMARY KEY auto_increment,
  expense_id INT NOT NULL,
  product_purchased INT NOT NULL, 
  amount FLOAT NOT NULL DEFAULT 0.00,
  short_desc VARCHAR(200),
  is_active VARCHAR(10) NOT NULL DEFAULT 'ACTV',
  create_by VARCHAR(100) NOT NULL,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_update_date DATETIME ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_expensedetails_id
  FOREIGN KEY (expense_id) REFERENCES expense(id)
);

CREATE TABLE IF NOT EXISTS payment_details (
  id INT PRIMARY KEY auto_increment,
  expense_id INT NOT NULL,
  paid_via INT NOT NULL, 
  amount_paid FLOAT NOT NULL DEFAULT 0.00,
  is_active VARCHAR(10) NOT NULL DEFAULT 'ACTV',
  create_by VARCHAR(100) NOT NULL,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_update_date DATETIME ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_paymentdetails_expense_id
  FOREIGN KEY (expense_id) REFERENCES expense(id),
  CONSTRAINT fk_paymentdetails_paid_id
  FOREIGN KEY (paid_via) REFERENCES payment_mode(id)
);