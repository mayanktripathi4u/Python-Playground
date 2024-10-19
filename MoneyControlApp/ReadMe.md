# MoneyControl App
To create a MoneyControl app with the specified requirements using Flask, Flask-SQLAlchemy, and Blueprints, here's a comprehensive setup with the folder structure and code. This example includes user authentication, CRUD operations for master data, and basic reporting features.

## Requirement: 
* I want to create a MoneyControl App.
* Very first user should be able to get authenticated before connecting to the app.
* Once login, user will able to view all his related records and manage his money.
* User will able to add / update / delete the master data such as Category; SubCategory; Product; PayMode; Bank, etc table (models)
* User will be able to add his Expense and details such as what he purchased / shopping; from where and when, how much he paid in total; details like product name, qty, tag-price, amount paid for the product, tax, discount, description etc; payment details -- which card type (pay mode) used if split split amount or total amout paid.
* User shoud be able to add his income.
* User shoudl able to view in dashboard the monthly expense vs Income; spending by category etc.


## Folder Structure
money_control_app/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── subcategory.py
│   │   ├── product.py
│   │   ├── paymode.py
│   │   ├── bank.py
│   │   ├── expense.py
│   │   ├── income.py
│   │   └── user.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── models.py
│   │   ├── masterdata/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── models.py
│   │   ├── transactions/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── models.py
│   │   ├── dashboard/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   ├── errors/
│   │   ├── __init__.py
│   │   ├── handlers.py
│   │   └── errors.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── migrations/
│
├── tests/
│
├── .env
├── requirements.txt
└── run.py


# FLask Migrate
`pip install flask-migrate`




# How to run
 cd Desktop/Apps/GitHub_Repo  
 source .venv/bin/activate  
 cd Python-Playground/MoneyControlApp/backend
 python run.py    

# Check the Query in Terminal
 cd Python-Playground/MoneyControlApp/backend
 flask shell
 >>> from models.user import User
 >>> User.query.all()

 user = User.query.filter_by(username='admin').first()


from models.expense import Expense, ExpenseDetail, PaymentDetail
from models.category import Category
from models.subcategory import SubCategory
from models.product import Product 
from sqlalchemy import extract, func
from datetime import datetime

monthly_expenses = db.session.query(
    func.date_format(Expense.purchase_date, '%M').label('month_name'),  # Get month name
    func.extract('month', Expense.purchase_date).label('month'),
    func.sum(Expense.total_amount).label('total_spent')
).group_by(func.date_format(Expense.purchase_date, '%M'), func.extract('month', Expense.purchase_date)).order_by('month', func.min(Expense.purchase_date)).all()


obj = ExpenseDetail.query.all()
for row in obj:
    row.product_id

for row in obj:
    row.product.name

for row in obj:
    row.product.subcategory.name

for row in obj:
    row.product.subcategory.category.name

current_month = datetime.now().month
current_year = datetime.now().year

<!-- top_spending_category = db.session.query(Category.name, func.sum(ExpenseDetail.amount).label('total_spent')).join(
    ExpenseDetail, Category.id == ExpenseDetail.category_id
).filter(
    func.extract('month', ExpenseDetail.date) == current_month,
    func.extract('year', ExpenseDetail.date) == current_year
).group_by(Category.name).order_by(func.sum(ExpenseDetail.amount).desc()).first() -->

<!-- top_spending_category = db.session.query(
    Category.name,  # Get the category name
    func.sum(ExpenseDetail.amount_paid).label('total_spent')  # Sum the amount_paid in ExpenseDetail
).join(
    Product, ExpenseDetail.product_id == Product.id  # Join Product table via product_id in ExpenseDetail
).join(
    SubCategory, Product.subcategory_id == SubCategory.id  # Join SubCategory via subcategory_id in Product
).join(
    Category, SubCategory.category_id == Category.id  # Join Category via category_id in SubCategory
).filter(
    func.extract('month', ExpenseDetail.purchase_date) == current_month,  # Filter by current month
    func.extract('year', ExpenseDetail.purchase_date) == current_year  # Filter by current year
).group_by(
    Category.name  # Group by Category name
).order_by(
    func.sum(ExpenseDetail.amount_paid).desc()  # Order by total spent in descending order
).first()  # Get the top category -->


top_spending_category = db.session.query(
    Category.name,  # Get the category name
    func.sum(ExpenseDetail.amount_paid).label('total_spent')  # Sum the amount_paid in ExpenseDetail
).join(
    Product, ExpenseDetail.product_id == Product.id  # Join Product table via product_id in ExpenseDetail
).join(
    SubCategory, Product.subcategory_id == SubCategory.id  # Join SubCategory via subcategory_id in Product
).join(
    Category, SubCategory.category_id == Category.id  # Join Category via category_id in SubCategory
).join(
    Expense, ExpenseDetail.expense_id == Expense.id  # Join Expense table via expense_id in ExpenseDetail
).filter(
    func.extract('month', Expense.purchase_date) == current_month,  # Filter by current month in Expense
    func.extract('year', Expense.purchase_date) == current_year  # Filter by current year in Expense
).group_by(
    Category.name  # Group by Category name
).order_by(
    func.sum(ExpenseDetail.amount_paid).desc()  # Order by total spent in descending order
).first()  # Get the top category
top_spending_category


top_spending_category = db.session.query(
    Category.name,  # Get the category name
    func.sum(ExpenseDetail.amount_paid).label('total_spent')  # Sum the amount_paid in ExpenseDetail
).join(
    Product, ExpenseDetail.product_id == Product.id  # Join Product table via product_id in ExpenseDetail
).join(
    SubCategory, Product.subcategory_id == SubCategory.id  # Join SubCategory via subcategory_id in Product
).join(
    Category, SubCategory.category_id == Category.id  # Join Category via category_id in SubCategory
).join(
    Expense, ExpenseDetail.expense_id == Expense.id  # Join Expense table via expense_id in ExpenseDetail
).filter(
    func.extract('month', Expense.purchase_date) == current_month,  # Filter by current month in Expense
    func.extract('year', Expense.purchase_date) == current_year  # Filter by current year in Expense
).group_by(
    Category.name  # Group by Category name
).order_by(
    func.sum(ExpenseDetail.amount_paid).desc()  # Order by total spent in descending order
).limit(5).all()  # Get the top 5 category
top_spending_category


<!-- top_spending_product = db.session.query(Product.name, func.sum(ExpenseDetail.amount_paid).label('total_spent')).join(
    ExpenseDetail, Product.id == ExpenseDetail.product_id
).filter(
    func.extract('month', Expense.purchase_date) == current_month,  # Filter by current month in Expense
    func.extract('year', Expense.purchase_date) == current_year  # Filter by current year in Expense
).group_by(Product.name).order_by(func.sum(ExpenseDetail.amount_paid).desc()).first()
top_spending_product -->

top_spending_product = db.session.query(
    Category.name,  # Get the category name
    Product.name.label('product_name'),  # Get the product name
    func.sum(ExpenseDetail.amount_paid).label('total_spent')  # Sum the amount_paid in ExpenseDetail
).join(
    Product, ExpenseDetail.product_id == Product.id  # Join Product table via product_id in ExpenseDetail
).join(
    SubCategory, Product.subcategory_id == SubCategory.id  # Join SubCategory via subcategory_id in Product
).join(
    Category, SubCategory.category_id == Category.id  # Join Category via category_id in SubCategory
).join(
    Expense, ExpenseDetail.expense_id == Expense.id  # Join Expense table via expense_id in ExpenseDetail
).filter(
    func.extract('month', Expense.purchase_date) == current_month,  # Filter by current month in Expense
    func.extract('year', Expense.purchase_date) == current_year  # Filter by current year in Expense
).group_by(
    Category.name,  # Group by Category name
    Product.name  # Also group by Product name to include it in the result
).order_by(
    func.sum(ExpenseDetail.amount_paid).desc()  # Order by total spent in descending order
).limit(5).all()  # Get the top 5 categories
top_spending_product