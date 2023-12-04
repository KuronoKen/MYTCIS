import sqlite3

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

    conn.close()

def print_patient():
     # Connect to the database
    conn = sqlite3.connect('Database/patients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM DrugAllergySymptoms')
    usersdata = cursor.fetchall()

    if not usersdata:
        print("No data in the DrugAllergies table.")
    else:
        print("Printing patient data:")
        for patient in usersdata:
            print(patient)

    conn.close()

#insert_patient('Pooh', '67TheSecond', 'male','1990-05-15' , 'kriimson@example.com','0621234567', '1234567890123')

print_patient()