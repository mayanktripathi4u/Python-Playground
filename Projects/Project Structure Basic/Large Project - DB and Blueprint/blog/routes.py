from blog import blog
from flask import render_template
from app.models.post import Post 

@blog.route('/blog')
def blog():
    posts = Post.query.all()

    return render_template('posts/index.html', posts = posts)

