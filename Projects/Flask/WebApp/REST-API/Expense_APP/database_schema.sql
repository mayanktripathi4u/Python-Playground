-- Categories Table
CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- SubCategories Table
CREATE TABLE SubCategories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(id)
);

-- Products Table
CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subcategory_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (subcategory_id) REFERENCES SubCategories(id)
);

-- Cards Table
CREATE TABLE Cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT CHECK(type IN ('Credit', 'Debit', 'NetBanking', 'Cash')) NOT NULL
);

-- Expenses Table
CREATE TABLE Expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_date DATE NOT NULL,
    purchase_location TEXT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    sales_tax DECIMAL(10, 2) NOT NULL
);

-- ExpenseDetails Table
CREATE TABLE ExpenseDetails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (expense_id) REFERENCES Expenses(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

-- Payments Table
CREATE TABLE Payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER,
    card_id INTEGER,
    payment_amount DECIMAL(10, 2) NOT NULL,
    payment_type TEXT CHECK(payment_type IN ('Credit', 'Debit', 'NetBanking', 'Cash')) NOT NULL,
    FOREIGN KEY (expense_id) REFERENCES Expenses(id),
    FOREIGN KEY (card_id) REFERENCES Cards(id)
);
