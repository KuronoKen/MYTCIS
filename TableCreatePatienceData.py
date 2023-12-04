import sqlite3

# Connect to the database (creates a new one if it doesn't exist)
conn = sqlite3.connect('Database/patients.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table for users
cursor.execute('''
    CREATE TABLE Patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    sex VARCHAR(10) CHECK (sex IN ('male', 'female', 'other')) NOT NULL,           
    date_of_birth DATE NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(10) NOT NULL,
    id_number VARCHAR(13) UNIQUE NOT NULL
    
    );
''')
cursor.execute('''
    CREATE TABLE FoodAllergies (
        food_allergy_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        patient_id INT NOT NULL,
        food_allergy_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
    );
''')
cursor.execute('''
    CREATE TABLE DrugAllergies (
        drug_allergy_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        patient_id INT NOT NULL,
        drug_allergy_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
    );
''')
cursor.execute('''
    CREATE TABLE FoodAllergySymptoms (
        allergy_symptom_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        patient_id INT NOT NULL,
        allergy_id INT NOT NULL, 
        symptom_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
        FOREIGN KEY (allergy_id) REFERENCES FoodAllergies(food_allergy_id)
    );
''')
cursor.execute('''
    CREATE TABLE DrugAllergySymptoms (
        allergy_symptom_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        patient_id INT NOT NULL,
        allergy_id INT NOT NULL, 
        symptom_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
        FOREIGN KEY (allergy_id) REFERENCES DrugAllergies(drug_allergy_id)
    );
''')

cursor.execute('''
    CREATE TABLE PatientEvents (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        patient_id INTEGER NOT NULL,
        category VARCHAR(255) NOT NULL,
        event_title VARCHAR(255) NOT NULL,
        description TEXT,
        medicine_list TEXT,
        appointment_date DATETIME,
        event_date DATETIME NOT NULL,
        record_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
    );
''')

# cursor.execute('''
#     DROP TABLE IF EXISTS PatientEvents;
# ''')

# Commit the changes and close the connection
conn.commit()
conn.close()