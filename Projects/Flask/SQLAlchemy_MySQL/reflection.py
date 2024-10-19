from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/mysql_2_sqlalchemy'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

tbl_misc = db.Table('tbl_misc', db.metadata, autoload = True, autoload_with = db.engine)

@app.route('/')
def index():
    results = db.session.query(tbl_misc).all() 
    # Cannot directly use below code as this is a table object and not a Flask SQLAlchemy Object. Thus has to use session.  
    # tbl_misc.query.all()
    for rec in results:
        print(rec.misc_name)
    return ''

if __name__ == "__main__":
    app.run(debug = True)
