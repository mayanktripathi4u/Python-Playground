# Working with existing MySQL DB.
# In MySQL I have a Database Schema as "mysql_2_sqlalchemy".

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session, sessionmaker, Session, declarative_base
# from sqlalchemy import event, exec, select
import datetime

mysql_db_url = "mysql://root:''@localhost/mysql_2_sqlalchemy"
engine = create_engine(mysql_db_url, echo=True, pool_recycle = 3600)

# # Alternative way is
# engine = ('mysql+pymysql://root:''@localhost/mysql_2_sqlalchemy', echo=True)
 
Base = declarative_base()
Base.metadata.reflect(engine)
db_session = scoped_session(sessionmaker(bind=engine))

class Tbl_Todo(Base):
    __table__ = Base.metadata.tables['tbl_todo']

class Tbl_Misc(Base):
    __table__ = Base.metadata.tables['tbl_misc']

# Adding or Inserting data
todo_1 = Tbl_Todo(task="my first task", status = "New", start_date = datetime.datetime.now, end_date = datetime.datetime.now)
todo_2 = Tbl_Todo(task="my second task", status = "Open", start_date = datetime.datetime.now, end_date = datetime.datetime.now)

db_session.add_all([todo_1, todo_2])
db_session.commit() 
db_session.close()

# Run this in Terminal, with command "python main.py"