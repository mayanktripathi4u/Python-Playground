# What is SQLAlchemy?
1. SQLAlchemy is a well-regarded database toolkit and ORM (Object-Relational Mapper) implementation written in Python.
2. SQLAlchemy provides a generalized interface for creating and executing database code without needing to write SQL statements.
3. SQLAlchemy can be used with or without the ORM features. Any given project can choose to just use SQLAlchemy Core or both Core and the ORM.
4. A benefit many developers enjoy with SQLAlchemy is that it allows them to write Python COde in their project to map from the datbase schema to the applications's python objects, no SQL is required to create, maintai and query the datanase.
5. The mapping allows SQLAlchemy to handle the underlying database to developers can worj with their Python objects instead of writing bridge code to get data in and out of relational tables.

# Install and COnnecting SQLAlchemy
```
pip install Flask-SQLAlchemy
```

With Postgress
```bash
posygresql://scott:tiget@localhost/mydatabase
```

With MySQL
```bash
mysql://scott:tiger@localhost/mydatabase
```

With Oracle
```bash
oracle://scott:tiger@127.0.0.1:1521/sidname
```

Steps
1. Create a Database in MySQL say "mysql_db"
2. Install Library
3. Code 
   a. Note: database name in MySQL and in the Python Code (app.py --> app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:''@localhost/db_sql_alchemy" --> should be same
)
4. run below commands in Python Shell, this will create tables in MySQL Dtaabase.
   ```bash
    from app import db
    db.create_all()
   ```
5. Change the Class name to say "employee", and reun the commands in Python SHell. You should see the new "employee" table in MySQL.


# Use Flask-SQLAlchemy with existing MySQL Database.
Lets get used to our existing database and how to access it from SQLAlchemy. 
We could use some MySQL documentation tool to find a way around this. 
The start with something like this (note that it has nothing to do with Flask ask all ... yet)

```bash
#!/usr/bin/python
# -*- mode: python -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)


from sqlalchemy.orm import relationship, backref

class Users(Base):
    __table__ = Base.metadata.tables['users']


if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker, Query
    db_session = scoped_session(sessionmaker(bind=engine))
    for item in db_session.query(Users.id, Users.name):
        print item
```
In the line "engine =" you need to provide your path to your MySQL database, so that SQLAlchemy finds it. In my case I used a pre-existing sqlite3 database.

In the line "class Users(Base)" you need to use one of existing tables in your MySQL database. I knew that my sqlite3 database had a table named "users".

After this point, SQLalchemy knows how to connect to your MySQL database and it knows about one of the tables. You need now to add all the other tables that you care for. Finally, you need to specify relationships to SQLalchemy. Here I mean things like one-to-one, one-to-many, many-to-many, parent-child and so on. The SQLAlchemy web site contains a rather lenghty section about this.

After the line "if __name__ == '__main__'" just comes some test code. It will be executed if I don't import my python script, but run. Here you see that I create a DB session and is that for a very simply query.

Additional details.
Below are the steps I used for my app:

1. initiate a `db` object in the usual flask-alchemy manner:`db = SQLAlchemy(app)`. Note you'll need to set `app.config['SQLALCHEMY_DATABASE_URI'] = 'connection_string'` before that.

2. bind the declarative base to an engine: `db.Model.metadata.reflect(db.engine)`

3. Then you can use existing tables easily (eg. I have a table called BUILDINGS):
```bash
class Buildings(db.Model):
    __table__ = db.Model.metadata.tables['BUILDING']

    def __repr__(self):
        return self.DISTRICT
```
Now your `Buildings` class will follow the existing schema. You can try `   ` in a Python shell and see all the columns already listed.

Refer 
https://stackoverflow.com/questions/17652937/how-to-build-a-flask-application-around-an-already-existing-database 

https://www.youtube.com/watch?v=nry95Fm7z0g



# Use Flask-SQLAlchemy with existing SQLite Database
2 options
* Reflection
* Auto-Map

