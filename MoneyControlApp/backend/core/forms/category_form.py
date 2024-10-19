from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from models.subcategory import SubCategory
from models.category import Category
from wtforms_sqlalchemy.fields import QuerySelectField

# Form for Category
class CategoryForm(FlaskForm):
    name = StringField("Category", validators=[DataRequired()])
    submit_category = SubmitField('Add Category')

# Form for SubCategory
class SubCategoryForm(FlaskForm):
    name = StringField('Sub-Category Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    submit_subcategory = SubmitField('Add SubCategory')

# Form for Product
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    subcategory = SelectField('Sub-Category', choices=[], validators=[DataRequired()])
    submit_product = SubmitField('Add Product')

# Combined form
class CombinedForm(FlaskForm):
    category_name = StringField('Category Name')
    subcategory_name = StringField('Sub-Category Name')
    product_name = StringField('Product Name')
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    subcategory = SelectField('Sub-Category', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')

def category_dropdown():
    return Category.query

# SubCategoryForm with Category dropdown
class SubCategoryForm_v2(FlaskForm):
    name = StringField('Sub-Category Name', validators=[DataRequired()])
    
    # Dropdown populated with categories from the Category model
    category = QuerySelectField('Category', 
                                query_factory=lambda: Category.query.all(), 
                                get_label='name', 
                                allow_blank=False, 
                                validators=[DataRequired()])

    # category = QuerySelectField(query_factory=category_dropdown, 
    #                             get_label='id', 
    #                             allow_blank=True, 
    #                             validators=[DataRequired()])
    
    submit_subcategory = SubmitField('Add SubCategory')

# ProductForm with SubCategory dropdown
class ProductForm_v2(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    
    # Dropdown populated with subcategories from the SubCategory model
    subcategory = QuerySelectField('Sub-Category', 
                                   query_factory=lambda: SubCategory.query.all(), 
                                   get_label='name', 
                                   allow_blank=False, 
                                   validators=[DataRequired()])
    
    submit_product = SubmitField('Add Product')