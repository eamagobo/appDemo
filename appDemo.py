from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb+srv://eamagobo:12345@flaskapp.7lgdm.mongodb.net/?retryWrites=true&w=majority&appName=FlaskApp')
db = client['user_data']
collection = db['survey_responses']

@app.route('/')
def index():
    return render_template('survey_form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        total_income = request.form['total_income']
        expenses = {
            'utilities': request.form['utilities'],
            'entertainment': request.form['entertainment'],
            'school_fees': request.form['school_fees'],
            'shopping': request.form['shopping'],
            'healthcare': request.form['healthcare']
        }
        # Store data in MongoDB
        collection.insert_one({
            'age': age,
            'gender': gender,
            'total_income': total_income,
            'expenses': expenses
        })
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

#Creating dictionary that will be comprising the categories and amount consumed
class User:
    def __init__(self, age, gender, income, expenses):
        self.age = age
        self.gender = gender
        self.income = income
        self.expenses = expenses
    
    def to_dict(self):
        return{
            'age': self.age,
            'gender': self.gender,
            'income': self.income
            **self.expenses
        }

import csv
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb+srv://eamagobo:12345@flaskapp.7lgdm.mongodb.net/?retryWrites=true&w=majority&appName=FlaskApp')
db = client['survey']
collection = db['responses']

# List to store User objects
users = []

# Loop through MongoDB data and create User objects
for response in collection.find():
    user = User(
        age=response['age'],
        gender=response['gender'],
        income=response['income'],
        expenses=response['expenses']  # This is a dictionary like {'utilities': 100, 'entertainment': 50, etc.}
    )
    users.append(user)

# Write data to a CSV file
with open('survey_data.csv', 'w', newline='') as file:
    # Get the field names (column headers)
    fieldnames = ["age", "gender", "income", "utilities", "entertainment", "school_fees", "shopping", "healthcare"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Write headers

    for user in users:
        # Write each user's data as a dictionary
        writer.writerow(user.to_dict())
