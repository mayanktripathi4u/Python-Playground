from app.models import User

def get_user():
    # Logic to retrieve users from the database
    return User.query.all()

def create_user(data):
    # Logic to create a new user in the database
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return user
