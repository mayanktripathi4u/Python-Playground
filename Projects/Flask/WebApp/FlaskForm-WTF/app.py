from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Email, ValidationError

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "some_random_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    
    def validate_email(self, field):
        existing_email = FormData.query.filter_by(email = field.data).first()
        if existing_email:
            raise ValidationError("Email Already Taken.")
    
    submit = SubmitField('Submit')

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    email  = db.Column(db.String(100), nullable = False)

with app.app_context():
    db.create_all()

# Repeating forms in Flask with WTForms, FieldList and FormField
class RepetatingFormB(FlaskForm):
    b1 = StringField("B1 Label")
    b2 = StringField("B2 Label")

class RegularFormA(FlaskForm):
    a1 = StringField("A1 Label")
    a2 = FieldList(FormField(RepetatingFormB), min_entries=5)
    s = SubmitField("Submit Label")

@app.route("/repeatingform")
def repeatingFormFunc():
    form = RegularFormA()
    return render_template('repeating_form.html', form = form)

@app.route("/repeatingformsubmit", methods = ["POST"])
def formSubmitted():
    a = request.form["a1"]
    b = request.form
    br = { x: b[x] for x in b if "a2-" in x}

    return render_template("result.html", a = a, b = br) 

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()

    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        # save to database
        form_data = FormData(name=name, email=email)
        db.session.add(form_data)
        db.session.commit()

        return 'Success'

    return render_template('index.html', form = form)

if __name__ == "__main__":
    app.run(debug = True)



"""
To check what all methods does the library has we could connect the Python Shell and run the command

>>> import wtforms.validators as val
>>> dir(val)

"""