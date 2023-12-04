from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
import sqlite3
import jwt
app = Flask(__name__)
CORS(app)

# A secret key to sign the JWT (keep it secret and secure in a real-world scenario)
app.secret_key = 'XDDDDDDDDDXD'

# Database setup (SQLite in this example)
DATABASE = 'Database/users.db'

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        # Generate a JWT token with the user information
        token = jwt.encode({'username': username}, app.secret_key, algorithm='HS256')
        # Return the token to the client
        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'success': False})

# Patient Register Function

def insert_patient(first_name, last_name, sex, date_of_birth , email, phone, id_number):
    # Connect to the database
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()
    
    patient_data = (first_name, last_name, sex, date_of_birth , email, phone, id_number)
    cursor.execute('''
        INSERT INTO Patients (first_name, last_name, sex, date_of_birth , email, phone, id_number)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', patient_data)
    conn.commit()

    cursor.execute('SELECT * FROM Patients')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the Patients table.")
    else:
        print("Printing patient data:")
        for patient in usersdata:
            print(patient)
    patient_id = cursor.lastrowid
    conn.close()
    return patient_id


def insert_food_allergies(cursor, patient_id, allergies):
    for allergy in allergies:
        food_allergy_name = allergy['name']
        
        # Insert data into FoodAllergies table (food_allergy_id will auto-increment)
        cursor.execute('''
            INSERT INTO FoodAllergies (patient_id, food_allergy_name)
            VALUES (?, ?)
        ''', (patient_id, food_allergy_name))

        # Retrieve the food_allergy_id for the newly inserted allergy
        food_allergy_id = cursor.lastrowid

        symptoms = allergy.get('allergysymptoms', [])
        insert_food_symptoms(cursor, patient_id, food_allergy_id, symptoms)

def insert_food_symptoms(cursor, patient_id, food_allergy_id, symptoms):
    for symptom in symptoms:
        symptom_name = symptom

        # Insert data into FoodAllergySymptoms table
        cursor.execute('''
            INSERT INTO FoodAllergySymptoms (patient_id, allergy_id, symptom_name)
            VALUES (?, ?, ?)
        ''', (patient_id, food_allergy_id, symptom_name))

def insert_drug_allergies(cursor, patient_id, allergies):
    for allergy in allergies:
        drug_allergy_name = allergy['name']
        
        # Insert data into FoodAllergies table (food_allergy_id will auto-increment)
        cursor.execute('''
            INSERT INTO DrugAllergies (patient_id, drug_allergy_name)
            VALUES (?, ?)
        ''', (patient_id, drug_allergy_name))

        # Retrieve the food_allergy_id for the newly inserted allergy
        drug_allergy_id = cursor.lastrowid

        symptoms = allergy.get('allergysymptoms', [])
        insert_drug_symptoms(cursor, patient_id, drug_allergy_id, symptoms)

def insert_drug_symptoms(cursor, patient_id, drug_allergy_id, symptoms):
    for symptom in symptoms:
        symptom_name = symptom

        # Insert data into DrugAllergySymptoms table
        cursor.execute('''
            INSERT INTO DrugAllergySymptoms (patient_id, allergy_id, symptom_name)
            VALUES (?, ?, ?)
        ''', (patient_id, drug_allergy_id, symptom_name))

@app.route('/registerpatient',methods=['POST'])
def registernewpatience():
    data = request.get_json()

    patient_name = data.get('patient_name')
    patient_surname = data.get('patient_surname')
    sex = data.get('sex')
    date_of_birth = data.get('date_of_birth')
    email = data.get('email')
    phone_number = data.get('phone_number')
    social_id = data.get('social_id')
    food_allergies = data.get('food_allergies', [])
    drug_allergies = data.get('drug_allergies', [])

    # Call your existing function to insert data into the database
    
    patient_id = insert_patient(patient_name,patient_surname,sex,date_of_birth,email,phone_number,social_id)
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()
    insert_food_allergies(cursor,patient_id,food_allergies)

    insert_drug_allergies(cursor,patient_id,drug_allergies)
    conn.commit()
    
    cursor.execute('SELECT * FROM Patients')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the Patients table.")
    else:
        print("Printing patient data:")
        for patient in usersdata:
            print(patient)
    
    cursor.execute('SELECT * FROM FoodAllergies')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the Patients table.")
    else:
        print("Printing allergy data:")
        for patient in usersdata:
            print(patient)

    cursor.execute('SELECT * FROM FoodAllergySymptoms')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the Patients table.")
    else:
        print("Printing food symptom data:")
        for patient in usersdata:
            print(patient)

    conn.close()

    return jsonify({'message': 'Data successfully processed'})

@app.route('/get_patient_allergies_and_symptoms/<id_number>', methods=['GET'])
def get_patient_data_by_id_number(id_number):
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()
    # Use a JOIN operation to fetch data from Patients, FoodAllergies, and FoodAllergySymptoms tables
    # Fetch patient data, food allergies, and food symptoms using JOIN operations
    cursor.execute('''
        SELECT Patients.*, FoodAllergies.food_allergy_name AS food_allergy, FoodAllergySymptoms.symptom_name AS food_symptom
        FROM Patients
        LEFT JOIN FoodAllergies ON Patients.patient_id = FoodAllergies.patient_id
        LEFT JOIN FoodAllergySymptoms ON FoodAllergies.food_allergy_id = FoodAllergySymptoms.allergy_id
        WHERE Patients.id_number = ?
    ''', (id_number,))

    food_rows = cursor.fetchall()

    # Fetch drug allergies and drug symptoms using JOIN operations
    cursor.execute('''
        SELECT Patients.*, DrugAllergies.drug_allergy_name AS drug_allergy, DrugAllergySymptoms.symptom_name AS drug_symptom
        FROM Patients
        LEFT JOIN DrugAllergies ON Patients.patient_id = DrugAllergies.patient_id
        LEFT JOIN DrugAllergySymptoms ON DrugAllergies.drug_allergy_id = DrugAllergySymptoms.allergy_id
        WHERE Patients.id_number = ?
    ''', (id_number,))

    drug_rows = cursor.fetchall()

    patient_data = {}
    food_allergies_dict = {}
    drug_allergies_dict = {}


    # Process food allergy data
    for row in food_rows:
        patient_id, first_name, last_name, sex, date_of_birth, email, phone, id_number, food_allergy, food_symptoms = row
        symptoms_list = [symptom.strip() for symptom in food_symptoms.split(',')] if food_symptoms else []

        # Populate patient data
        patient_data['patient_id'] = patient_id
        patient_data['first_name'] = first_name
        patient_data['last_name'] = last_name
        patient_data['sex'] = sex
        patient_data['date_of_birth'] = date_of_birth
        patient_data['email'] = email
        patient_data['phone'] = phone
        patient_data['id_number'] = id_number

        if food_allergy not in food_allergies_dict:
            food_allergies_dict[food_allergy] = symptoms_list
        else:
            food_allergies_dict[food_allergy].extend(symptoms_list)

    # Process drug allergy data
    for row in drug_rows:
        _, _, _, _, _, _, _, _, drug_allergy, drug_symptoms = row
        symptoms_list = [symptom.strip() for symptom in drug_symptoms.split(',')] if drug_symptoms else []

        # Add drug allergy and symptoms to the drug_allergies array
        if drug_allergy not in drug_allergies_dict:
            drug_allergies_dict[drug_allergy] = symptoms_list
        else:
            drug_allergies_dict[drug_allergy].extend(symptoms_list)
    # Close the cursor and connection
    print(patient_data)
    print(food_allergies_dict)
    print(drug_allergies_dict)
    conn.close()
    return jsonify({'info':patient_data,'food_allergies': food_allergies_dict, 'drug_allergies': drug_allergies_dict})


def insert_patient_event(connection, patient_id, category, event_title, description, medicine_list, appointment_date, event_date):

    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO PatientEvents (
            patient_id, category, event_title, description, medicine_list, appointment_date, event_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (patient_id, category, event_title, description, medicine_list, appointment_date, event_date))


@app.route('/registertimeline',methods=['POST'])
def registertimeline():
    data = request.get_json()
    patient_id = data.get('patient_id')
    category = data.get('category')
    event_title = data.get('event_title')
    description = data.get('description')
    medicine_list = data.get('medicine_list')
    appointment_date = data.get('appointment_date')
    event_date = data.get('event_date')
    # record_date = data.get('record_date')

    # Call your existing function to insert data into the database
    
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()
    insert_patient_event(conn,patient_id,category,event_title,description,medicine_list,appointment_date,event_date)

    conn.commit()
    
    cursor.execute('SELECT * FROM PatientEvents')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the Patients table.")
    else:
        print("Printing patient data:")
        for patient in usersdata:
            print(patient)

    conn.close()

    return jsonify({'message': 'Data successfully processed'})

@app.route('/get_patient_timeline/<patient_id>', methods=['GET'])
def getTimeline(patient_id):
    
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    connection = sqlite3.connect('Database/patients.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM PatientEvents WHERE patient_id = ?', (patient_id,))
    events = cursor.fetchall()

    connection.close()

    # Convert the events to a list of dictionaries for JSON serialization
    events_list = []
    for event in events:
        event_dict = {
            'event_id': event[0],
            'patient_id': event[1],
            'category': event[2],
            'event_title': event[3],
            'description': event[4],
            'medicine_list': event[5],
            'appointment_date': event[6],
            'event_date': event[7],
            'record_date': event[8],
        }
        events_list.append(event_dict)

    return jsonify({'events': events_list})

if __name__ == '__main__':
    app.run(debug=True)



