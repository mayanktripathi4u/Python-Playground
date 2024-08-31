# Let’s setup our project
We’ll start by creating an empty folder for our project, opening it in our text editor and adding a app.py file.

```
flaskapp
   app.py
```
Then we’ll install Flask..

`pip install flask`

and finally, we’ll create a simple app and start our server just to make sure things are setup right. We’ll start by importing the Flask class and then creating and instance of our WSGI application by using the __name__ shortcut.

After our first route we will call app.run() to start our server when the script is executed.

```
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'
if __name__ == '__main__':
    app.run(debug=True)
```

Now to run our server..
```
python3 app.py
```

You’re application should now be running on port 5000.

Another way we can run our server is to use the “flask run” command. For this we will first have to tell our terminal which application to work with by exporting the FLASK_APP environment variable and then calling flask run.

For windows CMD
```
set FLASK_APP=main
flask run
 * Running on http://127.0.0.1:5000/
```

# Adding Flask RESTful
Alright now its time to create our API using FlaskRESTful.

We’ll start by first installing FlaskRESTful, then modifying our routes to return some JSON data.

`pip install flask-restful`

In main.py import Resource & API from flask_restful, then create an instance of the Api class.

We will update our routes to use class base views now and inherit from Resource. These class based views will help us make our API more restful by separating our logic by the type of http method. For now each view will only process “get” requests

```
from flask import Flask
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)
fakeDatabase = {
    1:{'name':'Clean car'},
    2:{'name':'Write blog'},
    3:{'name':'Start stream'},
}
class Items(Resource):
    def get(self):
        return fakeDatabase
class Item(Resource):
    def get(self, pk):
        return fakeDatabase[pk]
api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')
if __name__ == '__main__':
    app.run(debug=True)
```

## Create Read, Update & Delete
Lets start by handling post requests so we can add data to our placeholder database.

*POST*

First we want to import “request” so we can read the data that's sent over in the request body
```
from flask import Flask, request
class Items(Resource):
    def get(self):
        return fakeDatabase 
    def post(self):
        data = request.json
        itemId = len(fakeDatabase.keys()) + 1
        fakeDatabase[itemId] = {'name':data['name']}
        return fakeDatabase
```

*PUT*
```
class Item(Resource):
    def get(self, pk):
        return fakeDatabase[pk]
    def put(self, pk):
        data = request.json
        fakeDatabase[pk]['name'] = data['name']
        return fakeDatabase
```
*Delete*
```
class Item(Resource):
    def get(self, pk):
        return fakeDatabase[pk]
    def put(self, pk):
        data = request.json
        fakeDatabase[pk]['name'] = data['name']
        return fakeDatabase
    def delete(self, pk):
        del fakeDatabase[pk]
        return fakeDatabase
```

Refer full article [at](https://medium.com/@dennisivy/flask-restful-crud-api-c13c7d82c6e5#:~:text=There%20are%20several%20ways%20we,we%20need%20for%20building%20API's.)
