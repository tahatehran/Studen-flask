from flask import Flask, jsonify, request, render_template, abort # type: ignore
import json
import os

app = Flask(__name__)
DATA_FILE = 'students.json'

if not os.path.exists(DATA_FILE):
    initial_data = [
        {"id": 1, "name": "sina", "lastname":"bahmani", "age": 21},
        {"id": 2, "name": "tiba", "lastname":"bahmani", "age": 22},
        {"id": 3, "name": "sara", "lastname":"bahmani", "age": 23},
        {"id": 4, "name": "taha", "lastname":"bahmani", "age": 20},
    ]
    with open(DATA_FILE, 'w') as f:
        json.dump(initial_data, f, indent=4)

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

#  وب سرویس نمایش تمام دانشجویان
@app.route('/students', methods=['GET'])
def get_all_students():
    data = read_data()
    return jsonify(data), 200

#  وب سرویس نمایش دانشجو بر اساس ID
@app.route('/student', methods=['POST'])
def get_student_by_id():
    student_id = request.form.get('id')
    if not student_id:
        abort(400)
    student_id = int(student_id)
    data = read_data()
    student = next((student for student in data if student['id'] == student_id), None)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student), 200

#  وب سرویس اضافه کردن دانشجو
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    lastname = request.form.get('lastname')
    age = request.form.get('age')
    if not name or not lastname or not age:
        abort(400)
    new_student = {
        'id': None,  
        'name': name,
        'lastname': lastname,
        'age': int(age)
    }
    data = read_data()
    new_student['id'] = len(data) + 1
    data.append(new_student)
    write_data(data)
    return jsonify(new_student), 201

if __name__ == '__main__':
    app.run(debug=True)
