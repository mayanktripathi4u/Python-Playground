from core import core
from flask import render_template, redirect, session, url_for, flash, jsonify, request
# from models.user import User
from models.category import Category
from models.subcategory import SubCategory
from models.product import Product 
from datetime import datetime
from models import db
from core.forms.category_form import CategoryForm, ProductForm, SubCategoryForm, ProductForm_v2, SubCategoryForm_v2
from sqlalchemy import extract, func
from sqlalchemy.exc import IntegrityError
from models.expense import Expense, ExpenseDetail, PaymentDetail
from models.income import Income
from models.paymode import PayMode
from core.forms.expense_form import ExpenseDetailForm, ExpenseForm

# Get current date and month
current_month = datetime.now().month
current_year = datetime.now().year

def top_5_category_products():
    top_spending_product = db.session.query(
        Category.name.label('category_name'),  # Get the category name
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
    return top_spending_product

def card_usage():
    card_usage_amount = 0
    return card_usage_amount


@core.route('/core/dashboard', methods = ['GET']) 
def dashboard():
    print(session['user_email'])
    print(session['user_name'])
    # Get current date and month
    current_month = datetime.now().month
    current_year = datetime.now().year

    if "user_name" not in session:
        return redirect(url_for('auth.login'))
    
    # Total expenses for current month
    total_expenses = db.session.query(func.sum(Expense.total_amount)).filter(
        func.extract('month', Expense.purchase_date) == current_month,
        func.extract('year', Expense.purchase_date) == current_year
    ).scalar() or 0
    total_expenses = float("{:.2f}".format(total_expenses))

    # Total income for current month
    # total_income = db.session.query(func.sum(Income.amount)).filter(
    #     func.extract('month', Income.received_date) == current_month,
    #     func.extract('year', Income.received_date) == current_year
    # ).scalar() or 0
    # total_income = float("{:.2f}".format(total_income))
    total_income = 6000

    # Calculate the balance (assuming opening balance is stored somewhere)
    opening_balance = 1000  # You should replace this with actual logic to fetch the opening balance
    current_balance = opening_balance + total_income - total_expenses

    # Get the top spending category for the current month
    # top_spending_category = db.session.query(Category.name, func.sum(ExpenseDetail.amount).label('total_spent')).join(
    #     ExpenseDetail, Category.id == ExpenseDetail.category_id
    # ).filter(
    #     func.extract('month', ExpenseDetail.date) == current_month,
    #     func.extract('year', ExpenseDetail.date) == current_year
    # ).group_by(Category.name).order_by(func.sum(ExpenseDetail.amount).desc()).first()

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
    
    # Expense trend (for chart)
    # monthly_expenses = db.session.query(
    #     func.date_format(Expense.purchase_date, '%M').label('month_name'),  # Get month name
    #     func.extract('month', Expense.purchase_date).label('month'),
    #     func.sum(Expense.total_amount).label('total_spent')
    # ).group_by(func.date_format(Expense.purchase_date, '%M'), func.extract('month', Expense.purchase_date)).order_by('month', func.min(Expense.purchase_date)).all()

    # Filtering for Month-Year
    monthly_expenses = db.session.query(
        func.date_format(Expense.purchase_date, '%M-%Y').label('month_name'),  # Get month name and year
        func.extract('month', Expense.purchase_date).label('month'),
        func.extract('year', Expense.purchase_date).label('year'),
        func.sum(Expense.total_amount).label('total_spent')
    ).group_by(func.date_format(Expense.purchase_date, '%M-%Y'), func.extract('month', Expense.purchase_date), func.extract('year', Expense.purchase_date)).order_by('year', 'month', func.min(Expense.purchase_date)).all()


    top_spending_product = top_5_category_products()

    return render_template(
        'dashboard.html', 
        user_name = session['user_name'],
        total_expenses=total_expenses,
        total_income=total_income,
        opening_balance=opening_balance,
        current_balance=current_balance,
        top_spending_category=top_spending_category,
        monthly_expenses=monthly_expenses,
        top_spending_product = top_spending_product
    )

@core.route('/core/add_category', methods = ['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        print("add_category function is called.")
        name = form.name.data
        last_login = datetime.now()

        # Fetch the Category from the database by category name (making it to lower and compare.)
        existing = Category.query.filter(
                                            func.lower(Category.name) == func.lower(name),
                                            Category.active == 1
                                        ).first()

        if existing:
            flash("Category already exists! Try for Category.", "error")
            # return render_template('list_categories')
            # Note: This route handles AJAX requests using POST. If the category is successfully added, it returns a JSON response.
            return jsonify({'success': False, 'message': 'Category already exists!'})

        else:
            new_rec = Category(name=name)
            db.session.add(new_rec)
            db.session.commit()

        flash("Category Added Successfull! Please Proceed further.", "success")

        # return redirect(url_for('list_categories')) # Provide name of function
        return jsonify({'success': True, 'message': 'Category added successfully!'})

    return render_template('add_category.html', form = form)

@core.route('/core/add_subcategory', methods = ['GET', 'POST'])
def add_subcategory():
    form = SubCategoryForm()
    if form.validate_on_submit():
        print("add_subcategory function is called.")
        name = form.name.data
        last_login = datetime.now()

        # # Fetch the Category from the database by category name (making it to lower and compare.)
        # existing = Category.query.filter(
        #                                     func.lower(Category.name) == func.lower(name),
        #                                     Category.active == 1
        #                                 ).first()

        # if existing:
        #     flash("Category already exists! Try for Category.", "error")
        #     # return render_template('list_categories')
        #     # Note: This route handles AJAX requests using POST. If the category is successfully added, it returns a JSON response.
        #     return jsonify({'success': False, 'message': 'Category already exists!'})

        # else:
        #     new_rec = Category(name=name)
        #     db.session.add(new_rec)
        #     db.session.commit()

        flash("Category Added Successfull! Please Proceed further.", "success")

        # return redirect(url_for('list_categories')) # Provide name of function
        return jsonify({'success': True, 'message': 'Category added successfully!'})

    return render_template('add_category.html', form = form)


@core.route('/core/categories', methods = ['GET', 'POST'])
def list_categories():
    form = CategoryForm()
    # subcat_form = SubCategoryForm()
    # prd_form = ProductForm()

    # if request.method == 'POST':
    #     # Check if CategoryForm was submitted
    #     if form.validate_on_submit() and form.submit_category.data:
    #         name = form.name.data
    #         last_login = datetime.now()

    #         # Fetch the Category from the database by category name (making it to lower and compare.)
    #         existing = Category.query.filter(
    #                                             func.lower(Category.name) == func.lower(name),
    #                                             Category.active == 1
    #                                         ).first()

    #         if existing:
    #             flash("Category already exists! Try for different Category.", "error")
    #             # Note: This route handles AJAX requests using POST. If the category is successfully added, it returns a JSON response.
    #             return jsonify({'success': False, 'message': 'Category already exists!'})

    #         else:
    #             new_rec = Category(name=name)
    #             db.session.add(new_rec)
    #             db.session.commit()

    #         flash("Category Added Successfull! Please Proceed further.", "success")

    #         return jsonify({'success': True, 'message': 'Category added successfully!'})
        
    #     # Check if SubCategoryForm was submitted
    #     elif subcat_form.validate_on_submit() and subcat_form.submit_subcategory.data:
    #         name = subcat_form.name.data
    #         categoryID = subcat_form.category.data
    #         last_login = datetime.now()

    #         # Fetch the SubCategory from the database by SubCategory name (making it to lower and compare.)
    #         existing = SubCategory.query.filter(
    #                                             func.lower(SubCategory.name) == func.lower(name)
    #                                         ).first()

    #         if existing:
    #             flash("SubCategory already exists! Try for different SubCategory.", "error")
    #             # Note: This route handles AJAX requests using POST. If the SubCategory is successfully added, it returns a JSON response.
    #             return jsonify({'success': False, 'message': 'SubCategory already exists!'})

    #         else:
    #             new_rec = SubCategory(name=name, category_id = categoryID)
    #             db.session.add(new_rec)
    #             db.session.commit()

    #         flash("SubCategory Added Successfull! Please Proceed further.", "success")

    #         return jsonify({'success': True, 'message': 'SubCategory added successfully!'})
        
    #     # Check if ProductForm was submitted
    #     elif prd_form.validate_on_submit() and prd_form.submit_product.data:
    #         name = prd_form.name.data
    #         subcategoryID = prd_form.subcategory.data
    #         last_login = datetime.now()

    #         # Fetch the Product from the database by Product name (making it to lower and compare.)
    #         existing = Product.query.filter(
    #                                             func.lower(Product.name) == func.lower(name)
    #                                         ).first()

    #         if existing:
    #             flash("Product already exists! Try for different Product.", "error")
    #             # Note: This route handles AJAX requests using POST. If the Product is successfully added, it returns a JSON response.
    #             return jsonify({'success': False, 'message': 'Product already exists!'})

    #         else:
    #             new_rec = Product(name=name, subcategory_id = subcategoryID)
    #             db.session.add(new_rec)
    #             db.session.commit()

    #         flash("Product Added Successfull! Please Proceed further.", "success")

    #         return jsonify({'success': True, 'message': 'Product added successfully!'})

    categories = Category.query.all()  # Fetch all categories
    # return render_template('categories_list.html', categories=categories, form = form)
    return render_template('categories.html', categories=categories, form = form)


@core.route('/core/v2/categories', methods = ['GET', 'POST'])
def list_categories_v2():
    cat_form = CategoryForm()
    subcat_form = SubCategoryForm_v2()
    # subcat_form.category.query = Category.query.all() 
    prd_form = ProductForm_v2()

    print("/core/v2/categories URL is hit, and the function list_categories_v2 is called.")

    if request.method == 'POST':
        # Check if CategoryForm was submitted
        if cat_form.submit_category.data and cat_form.validate_on_submit():
            print("Category Form is Submitted with below data ---------> \n")
            category_name = cat_form.name.data
            print(category_name)
            new_category = Category(name=category_name)
            
            try:
                db.session.add(new_category)
                db.session.commit()
                flash('Category added successfully!', 'success')
            except IntegrityError:
                db.session.rollback()  # Rollback the transaction
                flash(f'Category "{category_name}" already exists!', 'danger')

            # flash('Category added successfully!', 'success')
            return redirect(url_for('core.list_categories_v2'))
        
        # Check if SubCategoryForm was submitted
        elif subcat_form.submit_subcategory.data and subcat_form.validate_on_submit():
            subcategory_name = subcat_form.name.data
            category = subcat_form.category.data # This is the selected category from the dropdown
            category_id = category.id
            print(f"Sub-Category Form is Submmited with following details {subcategory_name} and {category} --> {category_id}. Verify it before adding.")
            new_subcategory = SubCategory(name=subcategory_name, category_id = category_id)
            
            try:
                db.session.add(new_subcategory)
                db.session.commit()
                flash('Subcategory added successfully!', 'success')
            except IntegrityError:
                db.session.rollback()  # Rollback the transaction
                flash(f'Subcategory "{subcategory_name}" already exists!', 'danger')

            # flash('Sub-Category added successfully!', 'success')
            return redirect(url_for('core.list_categories_v2'))
        
        # Check if ProductForm was submitted
        elif prd_form.submit_product.data and prd_form.validate_on_submit():
            product_name = prd_form.name.data
            subcategory = prd_form.subcategory.data  # This is the selected subcategory from the dropdown
            subcategory_id = subcategory.id
            print(f"Product Form is Submmited with following details {product_name} and {subcategory} --> {subcategory_id}. Verify it before adding.")
            new_product = Product(name=product_name, subcategory_id = subcategory_id)
            
            try:
                db.session.add(new_product)
                db.session.commit()
                flash('Product added successfully!', 'success')
            except IntegrityError:
                db.session.rollback()  # Rollback the transaction
                flash(f'Product "{product_name}" already exists!', 'danger')

            # flash('Product added successfully!', 'success')
            return redirect(url_for('core.list_categories_v2'))

    categories = Category.query.all()  # Fetch all categories 
    return render_template('categories_v2.html', categories = categories, cat_form = cat_form, subcat_form = subcat_form, prd_form = prd_form)

@core.route('/core/v2/test', methods = ['GET', 'POST'])
def test_queryselectfield():
    subcat_form = SubCategoryForm_v2()
    if subcat_form.validate_on_submit():
        subcategory_name = subcat_form.name.data
        category_id = subcat_form.category.data # This is the selected category from the dropdown
        print(f"Sub-Category Form is Submmited with following details {subcategory_name} and {category_id}. Verify it before adding.")

        return '<html><h1>{}</h1></html>'.format(category_id)
    
    return render_template('test.html', subcat_form = subcat_form)

@core.route('/core/add_expense', methods=['GET', 'POST'])
def add_expense():
    # if "user_name" not in session:
    #     return redirect(url_for('auth.login'))
    
    form = ExpenseForm()

    # Query to get expenses for the current month
    # current_month_expenses = Expense.query.filter(
    #     extract('month', Expense.purchase_date) == datetime.now().month,
    #     extract('year', Expense.purchase_date) == datetime.now().year,
    #     Expense.user_id == session['user_id']
    # ).all()

    # Handle form submission for adding an expense
    print(f"Expense: CHeck if form is valid --> {form.validate_on_submit()}")
    print(f"Expense: Check of form is submitted with data --> {form.submit_expense.data}")

    if form.validate_on_submit():
        # Proceed with adding the expense
        print("Expense: Form validated successfully")
    else:
        print(f"Expense: form.errors : {form.errors}")  # Print validation errors

    if form.validate_on_submit() and form.submit_expense.data:
        print("received Users expense data")
        expense = Expense(
            user_id = session['user_id'],  # Assuming you have a user login system
            purchase_from=form.purchase_from.data,
            purchase_date=form.purchase_date.data or datetime.now(),
            total_amount=form.total_amount.data,
            description=form.description.data
        )
        print(f"User entered expsnes as {expense}")
        db.session.add(expense)
        db.session.commit()

        # Add PaymentDetails
        for payment_form in form.payment_details:
            print("Adding Payment Details")
            payment_detail = PaymentDetail(
                expense_id=expense.id,
                pay_mode=payment_form.pay_mode.data,
                amount_paid=payment_form.amount_paid.data
            )
            print(f"User entered Payment Details as {payment_detail}")
            db.session.add(payment_detail)

        db.session.commit()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('core.add_expense'))
    
    # Handle search submission
    search_results = None
    print(f"Value of search_results : {search_results}")
    print(f"Check if form.submit_search.data : {form.submit_search.data}")
    print(f"Check if form.validate(): {form.validate()}")

    # if form.validate():
    #     # Proceed with adding the expense
    #     print("Form validated successfully")
    # else:
    #     print(f"form.errors : {form.errors}")  # Print validation errors

    # if form.submit_search.data and form.validate():
    if form.submit_search.data:
        print(f"Search Button is hit and form validated.")
        query = Expense.query.filter_by(user_id=session['user_id'])

        # Filter by search query for 'purchase_from'
        if form.search_query.data:
            query = query.filter(Expense.purchase_from.ilike(f"%{form.search_query.data}%"))

        # Filter by date range
        if form.start_date.data and form.end_date.data:
            query = query.filter(Expense.purchase_date.between(form.start_date.data, form.end_date.data))

        search_results = query.all()
    else:
        search_results = Expense.query.filter(
            extract('month', Expense.purchase_date) == datetime.now().month,
            extract('year', Expense.purchase_date) == datetime.now().year,
            Expense.user_id == session['user_id']
        ).all()

        print(f"Search Result : {search_results}")

    # expenses = Expense.object.all()
    if search_results :
        for expense in search_results:
            print(f"Expense from {expense.purchase_from} on {expense.purchase_date}")

        
        for payment_detail in expense.payment_details:
            print(f"  Payment Mode: {payment_detail.pay_mode}, Amount Paid: {payment_detail.amount_paid}")
    
    return render_template('add_expenses.html', form=form, search_results = search_results)


@core.route('/core/expense/<int:expense_id>/details', methods=['GET', 'POST'])
def add_expense_details(expense_id):
    print(f"Function add_expense_details() called, with Expense ID as {expense_id}")
    expense = Expense.query.get_or_404(expense_id)
    form = ExpenseDetailForm()

    # Fetch the current expense details for the given expense
    expense_details = ExpenseDetail.query.filter_by(expense_id=expense_id).all()

    # Query to calculate the total amount_paid for the given expense_id
    total_amount = db.session.query(func.sum(ExpenseDetail.amount_paid)).filter_by(expense_id=expense_id).scalar()
    print(f"Expense Detail for expense_id {expense_id} ==> Total Amount : {total_amount}")
    if total_amount:
        total_amount = float("{:.2f}".format(total_amount))
    else:
        total_amount = 0.00

    if form.validate_on_submit():
        expense_detail = ExpenseDetail(
            expense_id=expense_id,
            product_id=form.product_id.data,
            quantity=form.quantity.data,
            amount_paid=form.amount_paid.data,
            discount=form.discount.data,
            description=form.description.data
        )
        db.session.add(expense_detail)
        db.session.commit()
        flash('Expense Detail added successfully!', 'success')
        return redirect(url_for('core.add_expense_details', expense_id=expense_id))

    return render_template('add_expense_details.html', form=form, expense=expense, expense_details = expense_details, total_amount = total_amount)


@core.route('/core/autocomplete_product', methods=['GET'])
def autocomplete_product():
    search = request.args.get('q')
    print(f"autocomplete for product is working in {search} characters.")
    products = Product.query.filter(Product.name.like(f"%{search}%")).all()
    product_list = [{"id": p.id, "name": p.name} for p in products]
    return jsonify(product_list)


@core.route('/core/expense/<int:expense_id>/edit', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if "user_name" not in session:
        return redirect(url_for('auth.login'))
    
    print(f"Function edit_expense() called, with Expense ID as {expense_id}")
    expense = Expense.query.get_or_404(expense_id)
    form = ExpenseForm(obj = expense)

    return redirect(url_for('core.add_expenses', form = form))
