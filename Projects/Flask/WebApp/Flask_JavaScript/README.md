# Connecting Flask and JavaScript: Calling Python Functions
Flask is a micro web framework for Pythin, offering powerful tools for seamless web development. One common task in we applications is to call backend python functions in respinse to frontwend events suhc as clicking a button. This process often requires integration between Flask for the backend and javascript for the frontend. Here, we will explore how to accomlish this.

# Setting Up Flask
First we need to set up a basic Flask application. If you havent already installed Flask, you can do so using pip.

`pip install Flask`

Next, create a [Flask application](/Python-Playground/Projects/Flask/WebApp/Flask_JavaScript/app.py).

```
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
...
....
```

In above code
* we create a root route `(/)` that renders `index.html`.
* We define another route `(/call_function)` that accepts POST requests and calls a pythin function.
* There`your_python_function` is a dummy function that doubles the value sent from the client.

# Creating the HTML and JavaScript
The next step involves creating an HTML file with a nutton and some JavaScript code to handle the button click event.

[index.html](/Python-Playground/Projects/Flask/WebApp/Flask_JavaScript/index.html)

In this HTML
* A button triggers the "callPythonFunction" Javascript function on click.
* The JS function sends a POST request to the /call_function endpoint using the Fetch API.
* The response form the servre is handled to display the result in a div with the ID result.

# Running the App
After setting up the backend and frontend, you can run your Flask app. by executing the following command.

`pythin app.py`

Navigate to http://127.0.0.1:5000 in your browser, click the button and observe the console log and result displayed on the webpage.

# COnclusion
Combining Flask fir the backend with JS for the frontend alows you to create dynamic web app that can interact seamlessly. This basic example demo how to call a pthon function from a JS button clieck event, paving the way for more compex interactions in your web projects.

