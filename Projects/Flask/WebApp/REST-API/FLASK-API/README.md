Using the Virtual Env. same as from "REST-API/CRUD/"

```
pip install flask flask_restful flask_sqlalchemy
```

```
pip freeze > requirements.txt
```

```
touch .gitignore
```

Next create a "api.py" file, to just have a code to test.
```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Flask REST API</h1>"

if __name__ == "__main__":
    app.run(debug=True)
```
Run the command in terminal
```
python3 api.py
```
Open the browser, and use the URL to view the page http://127.0.0.1:5000

Next is to add more code related to Database, so define the `app.config()` to point our application with the specificed database and also define the database model class as `UserModel`.
Before re-running our code to run the script `python3 api.py`, we have to create the database, for this use the script [create_db.py](/Python-Playground/Projects/Flask/WebApp/REST-API/FLASK-API/create_db.py) and run it `python3 create_db.py` which will create a database for us path will be "/instance/database.db".

Next is to do a get / post request. From browser we do do get request, however for post request we would need some third-party such as `Postman`, `Thunder Client` (it has VS Code Extension), `curl command` etc.

http://127.0.0.1:5000/api/users/
http://127.0.0.1:5000/api/user/3

CURL Command:
```
curl -X POST http://127.0.0.1:5000/api/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Mayank", "email": "abc@abc.com"}'
```