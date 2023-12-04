import sqlite3

def insert_allergy(patient_id, drug_allergy_name, symptom_name):
    # Connect to the database
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()

    # Insert data into DrugAllergies table
    cursor.execute('''
        INSERT INTO DrugAllergies (patient_id, drug_allergy_name)
        VALUES (?, ?)
    ''', (patient_id, drug_allergy_name))

    drug_allergy_id = cursor.lastrowid

    # Insert data into DrugAllergySymptoms table
    cursor.execute('''
        INSERT INTO DrugAllergySymptoms (patient_id, allergy_id, symptom_name)
        VALUES (?, ?, ?)
    ''', (patient_id, drug_allergy_id, symptom_name))

    conn.commit()

    conn.close()

def print_allergy():
     # Connect to the database
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM DrugAllergySymptoms')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the Patients table.")
    else:
        print("Printing DrugAllergySymptoms data:")
        for patient in usersdata:
            print(patient)

    cursor.execute('SELECT * FROM DrugAllergies')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the Patients table.")
    else:
        print("Printing allergy data:")
        for patient in usersdata:
            print(patient)

    conn.close()

insert_allergy(1,'Paracetamol','Headache')

print_allergy()