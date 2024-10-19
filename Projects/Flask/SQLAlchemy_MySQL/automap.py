from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/mysql_2_sqlalchemy'

db = SQLAlchemy(app)

BASE = automap_base()
BASE.prepare(db.engine, reftect=True)

with app.app_context():
    db.create_all()

tbl_todo = BASE.classes.tbl_todo

@app.route('/')
def index():
    new_record = tbl_todo(task = "My FIrst Task", status = "New", start_date = '2024-09-06', end_date = '2024-09-06')
    db.session.add(new_record)
    db.session.commit()

    # results = db.session.query(tbl_todo).all() 
    # # Cannot directly use below code as this is a table object and not a Flask SQLAlchemy Object. Thus has to use session.  
    # # tbl_misc.query.all()
    # for rec in results:
    #     print(rec.misc_name)
    return ''

if __name__ == "__main__":
    app.run(debug = True)
