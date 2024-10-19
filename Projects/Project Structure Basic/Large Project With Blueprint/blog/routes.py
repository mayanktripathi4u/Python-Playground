from blog import blog
from flask import render_template

@blog.route('/blog')
def blog():
    return render_template('index.html')

