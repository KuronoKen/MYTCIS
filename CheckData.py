import sqlite3

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
    cursor.close()
    conn.close()

# Example: Fetch data for a specific id_number
get_patient_data_by_id_number('5566797979979')
