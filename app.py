# app.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI
from cerberus import Validator


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course_payment_status = db.Column(db.Boolean, nullable=False)
    residence = db.Column(db.String(100), nullable=False)
    city_access_permit = db.Column(db.Boolean, nullable=False)
    course_registration_status = db.Column(db.Boolean, nullable=False)

# Create the database tables within a Flask application context
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

registration_schema = {
    'first_name': {'type': 'string', 'minlength': 1, 'maxlength': 50},
    'last_name': {'type': 'string', 'minlength': 1, 'maxlength': 50},
    'age': {'type': 'integer', 'min': 1},
    'course_payment_status': {'type': 'boolean'},
    'residence': {'type': 'string', 'minlength': 1, 'maxlength': 100},
    'city_access_permit': {'type': 'boolean'},
    'course_registration_status': {'type': 'boolean'}
}

#  A Validator instance
validator = Validator()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate the incoming data
    if not validator.validate(data, registration_schema):
        return jsonify({'error': 'Invalid data', 'details': validator.errors}), 400

    # Process the validated data
    student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        course_payment_status=data['course_payment_status'],
        residence=data['residence'],
        city_access_permit=data['city_access_permit'],
        course_registration_status=data['course_registration_status']
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({'message': 'Registration successful'})

if __name__ == '__main__':
    app.run(debug=True)
