from app import app
from blog import blog

app.register_blueprint(blog)

if __name__ == '__main__':
    app.run(debug = True)