# Money Control

## Setup
- Virtual Env Setup
  - Virtual Env.
  ```bash
    # For mac/linux
    python3 -m venv venv
    . ven/bin/activate

    # For Windows
    python3 -m venv venv
    venv\Scripts\activate
  ```
  - Flask Install
  ```bash
    pip install flask
  ```
- Run Flask App
  - Run the App
  ```bash
    # if the file name is not as app.py or wsgi.py.
    # Use `--app`
    flask --app hello run
  ```
  ```bash
    # if the file name is app.py or wsgi.py.
    flask run
  ```
  ```bash
    # To run in debug mode and reload on code change.
    # Use `--debug`.
    flask --debug run
  ```
  ```bash
    # To access in your network publically use `--host`.
    flask run --host=0.0.0.0
  ```
  

- Basic Routing
- 
- HTTP Client Tool for testing HTTP Requests
  - A `.http` file is typically used by certail IDE's (like JetBrains; PyCharm or Visual Studio Code with the REST client extension) to define and execute HTTP requests directly from the editor.
  - The file format allows you to write, test, and execute HTTP requests without needing to use tools like Postman or CURL separately.
  - Usage of `.http` file: 
    - Testing HTTP Requests: You can define GET; POST; PUT; DELETE etc. requests within this file, which can be run to interact with your Flask app or any other HTTP-based service.
    - Local Development: You might use this file to test endpoints of your Flask application during development.
  - [Refer]() for more details.
