SELECT * FROM moneycontrol_flaskapp.category WHERE id >= 1;
SELECT * FROM moneycontrol_flaskapp.sub_category WHERE id >= 1;
SELECT * FROM moneycontrol_flaskapp.product WHERE id >= 1;
SELECT * FROM moneycontrol_flaskapp.expense_detail WHERE id >= 1;
SELECT * FROM moneycontrol_flaskapp.expense WHERE id >= 1;
SELECT * FROM moneycontrol_flaskapp.pay_mode WHERE id >= 1;
SELECT * FROM moneycontrol_flaskapp.user WHERE id >= 1;
SELECT * FROM moneycontrol_flaskapp.payment_detail WHERE id >= 1;
SELECT * FROM moneycontrol_flaskapp.income WHERE id >= 1;


DELETE FROM moneycontrol_flaskapp.expense_detail WHERE id >= 1;
DELETE FROM moneycontrol_flaskapp.payment_detail WHERE id >= 1;
DELETE FROM moneycontrol_flaskapp.expense WHERE id >= 1;
DELETE FROM moneycontrol_flaskapp.product WHERE id >= 1;
DELETE FROM moneycontrol_flaskapp.sub_category WHERE id >= 1;
DELETE FROM moneycontrol_flaskapp.category WHERE id >= 1;
DELETE FROM moneycontrol_flaskapp.pay_mode WHERE id >= 1;
DELETE FROM moneycontrol_flaskapp.user WHERE id >= 1;
DELETE FROM moneycontrol_flaskapp.income WHERE id >= 1;
 

INSERT INTO moneycontrol_flaskapp.pay_mode (pay_mode, card_bank_name, card_nbr, active, create_date)
SELECT 'CC-Discover-425', 'Discover', 'XXX XXX XXX 425', 1, '2024-09-16 00:22:05' UNION 
SELECT 'CC-Citi-555', 'Citi', 'XXX XXX XXX 555', 1, '2024-09-16 00:22:05' UNION 
SELECT 'CC-AMX-009', 'American Express', 'XXX XXX XXX 009', 1, '2024-09-16 00:22:05' UNION 
SELECT 'GF-Walmart-578', 'Walmart', 'XXX XXX XXX 578', 1, '2024-09-16 00:22:05' UNION 
SELECT 'GF-Kroger-354', 'Kroger', 'XXX XXX XXX 354', 1, '2024-09-16 00:22:05' 

INSERT INTO moneycontrol_flaskapp.pay_mode (pay_mode, card_bank_name, card_nbr, active, create_date)
SELECT 'CC-WellsFargo-377', 'Wells Fargo', 'XXX XXX XXX 377', 1, '2024-09-16 00:22:05' 

INSERT INTO moneycontrol_flaskapp.pay_mode (pay_mode, card_bank_name, card_nbr, active, create_date)
SELECT 'DC-WellsFargo-137', 'Wells Fargo', 'XXX XXX XXX 137', 1, '2024-09-16 00:22:05' 