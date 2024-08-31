from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

db.create_all()

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    result = []
    for expense in expenses:
        result.append({
            'id': expense.id,
            'date': expense.date.strftime('%Y-%m-%d'),
            'description': expense.description,
            'amount': expense.amount,
            'category': expense.category
        })
    return jsonify(result)

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        date=data['date'],
        description=data['description'],
        amount=data['amount'],
        category=data['category']
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'})

@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    expense = Expense.query.get(id)
    if expense is None:
        return jsonify({'message': 'Expense not found'}), 404
    data = request.get_json()
    expense.date = data['date']
    expense.description = data['description']
    expense.amount = data['amount']
    expense.category = data['category']
    db.session.commit()
    return jsonify({'message': 'Expense updated successfully'})

@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense is None:
        return jsonify({'message': 'Expense not found'}), 404
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
    