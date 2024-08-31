from application import app
from flask import render_template

@app.route("/")
def index():
    # return "Hello from Application."
    return render_template('index.html', title = 'index')

@app.route("/layout")
def layout():
    return render_template("layout.html")

@app.route("/layout_dynamic")
def layout_dynamic():

    return render_template("layout_dynamic.html")
    # return render_template("layout_dynamic.html", title = 'layout')