from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy's automap library to reflect the existing database schema.
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/mysql_2_sqlalchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Print app --> {app}")

db = SQLAlchemy(app)

# print(f"Print the db.engine --> {db.engine}")

# Ensure that the database engine is properly created
# @app.before_first_request
@app.before_request
def create_db_engine():
    # This will ensure the engine is created and available
    print(f"Engine: {db.engine}")

# Reflect the existing database
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Session config to Access Tables
Session = scoped_session(sessionmaker(bind = db.engine))
# session = Session()

# Accessing the Tables
Todo = Base.classes.tbl_todo
Misc = Base.classes.tbl_misc


@app.route('/todo')
def get_todo_list():
    # todo = session.query(Todo).all()
    # print(f"Referencing the Table tbl_todo from SQLAlchemy {todo}")

    with app.app_context():
        session = Session()
        try:
            todo_list = session.query(Todo).all()
            # session.remove()  # Clean up the session
            return jsonify([{'task': t.task, 'status': t.status} for t in todo_list])
        
        finally:
            session.remove()  # Clean up the session
        

@app.route('/add_todo', methods = ['POST', 'GET'])
def add_todo():
    with app.app_context():
        session = Session()
        try: 
            todo_task   = 'New Task'    #request.json.get('task', 'default value')
            status      = 'OPEN'        #request.json.get('status', 'default value')
            start_date  = '2024-01-02'  #request.json.get('start_date', '2024-01-02')
            end_date    = '2024-03-03'  #request.json.get('end_date', '2024-02-02')

            new_obj = Base.classes.tbl_todo(task = todo_task, status = status, start_date = start_date, end_date = end_date)

            session.add(new_obj)
            session.commit()
            session.remove()  # Clean up the session
        finally:
            session.remove()  # Clean up the session
    
        return jsonify({'message': 'New TODO Task Added.'}), 201

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()  # Clean up any remaining sessions


if __name__ == '__main__':
    app.run(debug = True)