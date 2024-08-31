from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/call_function', method=['POST'])
def call_function():
    data = request.get_json # Call your Python Function Here.
    result = your_python_function(data)
    return jsonify(result=result)

def your_python_function(data):
    # sample function logic
    return data['value'] * 2

if __name__ == '__main__':
    app.run(debug = True)
    
