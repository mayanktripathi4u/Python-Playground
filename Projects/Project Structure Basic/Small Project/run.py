from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Home Page"

@app.route('/blog')
def blog():
    return "Blog Page"

if __name__ == "__main__":
    app.run(debug = True)