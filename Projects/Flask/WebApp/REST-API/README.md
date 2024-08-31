- [Flask REST API](#flask-rest-api)
- [Request method](#request-method)
- [Ways for creating a REST API in Flask](#ways-for-creating-a-rest-api-in-flask)
  - [Method 1: using only Flask](#method-1-using-only-flask)
  - [Method 2: Using flask-restful](#method-2-using-flask-restful)


# Flask REST API
REST stands for REpresentational State Transfer and is an architectural style used in modern web development.

It defines a set or rules /constraints for a web application to send and receive data.

REST API services let you intercat with the databases by simply doing HTTP requests.

In here we write a REST server using the Flask.


This is often how the backend of web apps is created. Returning data is in JSON format and requests we are using are `PUT`, `DELETE`, `POST`, and `GET`.

# Request method
We know that there are six commonly used HTTP request methods, which are
* GET
* POST
* PUT
* DELETE
* PATCH
* HEAD

The code that we just had had to deal with GET by default (the browser defaults to using `GET`), so how do you program the other requests?

Like this:
```
@app.route('/', methods=['POST'])
@app.route('/', methods=['DELETE'])
@app.route('/', methods=['PUT'])
```
The [program](/Python-Playground/Projects/Flask/WebApp/REST-API/example-request-method.py) will demonstrates this.

The code is long, but the code is easier to understand, and it is a relatively simple file operation.

# Ways for creating a REST API in Flask
There are several ways we can go about building API’s with Flask.

Flask RESTful is an extension for flask that adds extra features and gives us the tools we need for building API’s. For those of you that know Django think of it as what Django REST Framework is to Django.

In here will check for the two ways of creating a REST API in Flask.
1. Using Flask without any external libraries
2. Using flask_restful library

Technically you can build an API with just flask without any extra packages but Flask RESTful will make things easier so that's what I will use.

## Method 1: using only Flask
Lets start with the Development part, for this we will create two functions:
1. One function to just return or print the data sent through GET or POST 
2. Another function to calculate the square of a number sent through GET request and print it.

Refer [Code](/Python-Playground/Projects/Flask/WebApp/REST-API/BuildaRESTAPIusingFlask/method_1.py)

Run the Flask App usign command `python3 method_1.py` and use the curl command to check the response of API's.

```
curl http://127.0.0.1:5000/

curl http://127.0.0.1:5000/home/10
```

## Method 2: Using flask-restful
Flask Restful is an extension for Flask that adds support for building REST APIs in Python using Flask as the back-end. It encourages best practices and is very easy to set up. Flask restful is very easy to pick up if you’re already familiar with flask.

In flask_restful, the main building block is a resource. Each resource can have several methods associated with it such as GET, POST, PUT, DELETE, etc. for example, there could be a resource that calculates the square of a number whenever a get request is sent to it. Each resource is a class that inherits from the Resource class of flask_restful. Once the resource is created and defined, we can add our custom resource to the api and specify a URL path for that corresponding resource.

Refer [Code](/Python-Playground/Projects/Flask/WebApp/REST-API/BuildaRESTAPIusingFlask/method_2.py)

Run the Flask App usign command `python3 method_2.py` and use the curl command to check the response of API's.

```
curl http://127.0.0.1:5000/

curl http://127.0.0.1:5000/square/10
```

