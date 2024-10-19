MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'mysqlroot'
MYSQL_DB = 'moneycontrol_flaskapp'
MY_SECRET = "some_random_keys_type_here"
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
