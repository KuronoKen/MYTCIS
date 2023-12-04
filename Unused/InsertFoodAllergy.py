import sqlite3

def insert_allergy(patient_id, food_allergy_name, symptom_name):
    # Connect to the database
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()

    # Insert data into FoodAllergies table
    cursor.execute('''
        INSERT INTO FoodAllergies (patient_id, food_allergy_name)
        VALUES (?, ?)
    ''', (patient_id, food_allergy_name))

    food_allergy_id = cursor.lastrowid

    # Insert data into FoodAllergySymptoms table
    cursor.execute('''
        INSERT INTO FoodAllergySymptoms (patient_id, allergy_id, symptom_name)
        VALUES (?, ?, ?)
    ''', (patient_id, food_allergy_id, symptom_name))

    conn.commit()

    conn.close()

def print_allergy():
     # Connect to the database
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM FoodAllergySymptoms')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the Patients table.")
    else:
        print("Printing allergysymptom data:")
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

    conn.close()

insert_allergy(1,'Lactose','Ouch')

print_allergy()