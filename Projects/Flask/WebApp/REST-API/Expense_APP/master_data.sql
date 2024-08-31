-- -- Insert Categories
-- INSERT INTO Categories (name) VALUES ('Food');
-- INSERT INTO Categories (name) VALUES ('Electronics');
-- INSERT INTO Categories (name) VALUES ('Clothing');

-- -- Insert SubCategories
-- INSERT INTO SubCategories (category_id, name) VALUES (1, 'Groceries');
-- INSERT INTO SubCategories (category_id, name) VALUES (1, 'Dining Out');
-- INSERT INTO SubCategories (category_id, name) VALUES (2, 'Mobile Phones');
-- INSERT INTO SubCategories (category_id, name) VALUES (3, 'Men');
-- INSERT INTO SubCategories (category_id, name) VALUES (3, 'Women');

-- -- Insert Products
-- INSERT INTO Products (subcategory_id, name) VALUES (1, 'Milk');
-- INSERT INTO Products (subcategory_id, name) VALUES (1, 'Bread');
-- INSERT INTO Products (subcategory_id, name) VALUES (2, 'Restaurant A');
-- INSERT INTO Products (subcategory_id, name) VALUES (3, 'Smartphone A');
-- INSERT INTO Products (subcategory_id, name) VALUES (4, 'T-Shirt');
-- INSERT INTO Products (subcategory_id, name) VALUES (5, 'Dress');

-- -- Insert Cards
-- INSERT INTO Cards (name, type) VALUES ('Visa Card', 'Credit');
-- INSERT INTO Cards (name, type) VALUES ('MasterCard', 'Debit');
-- INSERT INTO Cards (name, type) VALUES ('PayPal', 'NetBanking');
-- INSERT INTO Cards (name, type) VALUES ('Cash', 'Cash');

-- -- Insert Payments
-- INSERT INTO Payments (expense_id, card_id, payment_amount, payment_type) VALUES (1, 1, 50.00, 'Credit');
-- INSERT INTO Payments (expense_id, card_id, payment_amount, payment_type) VALUES (1, 2, 25.00, 'Debit');
-- INSERT INTO Payments (expense_id, card_id, payment_amount, payment_type) VALUES (1, 4, 25.00, 'Cash');


-- Categories
INSERT INTO Categories (name) VALUES ('Food and Beverages');
INSERT INTO Categories (name) VALUES ('Housing');
INSERT INTO Categories (name) VALUES ('Transportation');
INSERT INTO Categories (name) VALUES ('Health and Insurance');
INSERT INTO Categories (name) VALUES ('Education');
INSERT INTO Categories (name) VALUES ('Entertainment');
INSERT INTO Categories (name) VALUES ('Clothing and Personal Care');
INSERT INTO Categories (name) VALUES ('Travel');
INSERT INTO Categories (name) VALUES ('Gifts and Donations');
INSERT INTO Categories (name) VALUES ('Miscellaneous');

-- SubCategories for Food and Beverages
INSERT INTO SubCategories (category_id, name) VALUES (1, 'Groceries');
INSERT INTO SubCategories (category_id, name) VALUES (1, 'Dining Out');
INSERT INTO SubCategories (category_id, name) VALUES (1, 'Snacks and Beverages');

-- Products for Groceries
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Milk');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Bread');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Eggs');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Vegetables');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Fruits');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Meat');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Rice');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Pasta');

-- Products for Dining Out
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Fast Food');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Casual Dining');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Fine Dining');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Coffee Shops');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Takeout');

-- Products for Snacks and Beverages
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Chips');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Sodas');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Juices');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Coffee');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Tea');

-- SubCategories for Housing
INSERT INTO SubCategories (category_id, name) VALUES (2, 'Rent/Mortgage');
INSERT INTO SubCategories (category_id, name) VALUES (2, 'Utilities');
INSERT INTO SubCategories (category_id, name) VALUES (2, 'Maintenance');

-- Products for Utilities
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Electricity');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Water');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Gas');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Internet');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Trash Collection');

-- Products for Maintenance
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Repairs');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Cleaning Supplies');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Gardening');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Pest Control');

-- SubCategories for Transportation
INSERT INTO SubCategories (category_id, name) VALUES (3, 'Fuel');
INSERT INTO SubCategories (category_id, name) VALUES (3, 'Public Transport');
INSERT INTO SubCategories (category_id, name) VALUES (3, 'Vehicle Maintenance');

-- Products for Fuel
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Gasoline');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Diesel');

-- Products for Public Transport
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Bus Tickets');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Train Passes');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Subway Tickets');

-- Products for Vehicle Maintenance
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Oil Changes');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Tire Replacement');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Car Wash');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Repairs');

-- SubCategories for Health and Insurance
INSERT INTO SubCategories (category_id, name) VALUES (4, 'Medical Expenses');
INSERT INTO SubCategories (category_id, name) VALUES (4, 'Health Insurance');
INSERT INTO SubCategories (category_id, name) VALUES (4, 'Fitness');

-- Products for Medical Expenses
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Doctor Visits');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Prescription Medications');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Over-the-Counter Medications');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Dental Visits');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Optometry Visits');

-- Products for Health Insurance
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Premiums');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Co-Pays');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Deductibles');

-- Products for Fitness
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Gym Membership');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Sports Equipment');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Fitness Classes');

-- SubCategories for Education
INSERT INTO SubCategories (category_id, name) VALUES (5, 'Tuition');
INSERT INTO SubCategories (category_id, name) VALUES (5, 'Books and Supplies');
INSERT INTO SubCategories (category_id, name) VALUES (5, 'Online Courses');

-- Products for Tuition
INSERT INTO Products (subcategory_id, name) VALUES (1, 'School Fees');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'College Fees');

-- Products for Books and Supplies
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Textbooks');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Notebooks');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Stationery');

-- Products for Online Courses
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Course Fees');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Subscription Services');

-- SubCategories for Entertainment
INSERT INTO SubCategories (category_id, name) VALUES (6, 'Movies and Shows');
INSERT INTO SubCategories (category_id, name) VALUES (6, 'Hobbies');
INSERT INTO SubCategories (category_id, name) VALUES (6, 'Events');

-- Products for Movies and Shows
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Cinema Tickets');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Streaming Subscriptions');

-- Products for Hobbies
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Books');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Music');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Crafts');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Video Games');

-- Products for Events
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Concerts');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Sports Events');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Festivals');

-- SubCategories for Clothing and Personal Care
INSERT INTO SubCategories (category_id, name) VALUES (7, 'Clothing');
INSERT INTO SubCategories (category_id, name) VALUES (7, 'Personal Care');
INSERT INTO SubCategories (category_id, name) VALUES (7, 'Laundry');

-- Products for Clothing
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Shirts');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Pants');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Dresses');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Shoes');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Accessories');

-- Products for Personal Care
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Haircuts');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Skincare Products');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Toiletries');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Makeup');

-- Products for Laundry
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Dry Cleaning');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Laundry Detergent');

-- SubCategories for Travel
INSERT INTO SubCategories (category_id, name) VALUES (8, 'Accommodation');
INSERT INTO SubCategories (category_id, name) VALUES (8, 'Transportation');
INSERT INTO SubCategories (category_id, name) VALUES (8, 'Activities');
INSERT INTO SubCategories (category_id, name) VALUES (8, 'Meals');

-- Products for Accommodation
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Hotels');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Airbnb');

-- Products for Transportation
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Flights');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Car Rentals');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Taxis');

-- Products for Activities
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Tours');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Excursions');

-- Products for Meals
INSERT INTO Products (subcategory_id, name) VALUES (4, 'Dining Out (Travel)');
INSERT INTO Products (subcategory_id, name) VALUES (4, 'Snacks');

-- SubCategories for Gifts and Donations
INSERT INTO SubCategories (category_id, name) VALUES (9, 'Gifts');
INSERT INTO SubCategories (category_id, name) VALUES (9, 'Donations');

-- Products for Gifts
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Birthdays');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Anniversaries');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Holidays');

-- Products for Donations
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Charities');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Fundraisers');

-- SubCategories for Miscellaneous
INSERT INTO SubCategories (category_id, name) VALUES (10, 'Subscriptions');
INSERT INTO SubCategories (category_id, name) VALUES (10, 'Office Supplies');
INSERT INTO SubCategories (category_id, name) VALUES (10, 'Bank Fees');

-- Products for Subscriptions
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Magazines');
INSERT INTO Products (subcategory_id, name) VALUES (1, 'Software');

-- Products for Office Supplies
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Printer Ink');
INSERT INTO Products (subcategory_id, name) VALUES (2, 'Paper');

-- Products for Bank Fees
INSERT INTO Products (subcategory_id, name) VALUES (3, 'Account Maintenance');
INSERT INTO Products (subcategory_id, name) VALUES (3, 'ATM Fees');

