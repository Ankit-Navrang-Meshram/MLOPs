import json
import random

def bmi(weight : float , height : float):
    weight_in_kg = weight
    height_in_meters = height / 100
    return (weight_in_kg / height_in_meters ** 2)

def verdict(bmi : float):
    if bmi < 18.5 :
        return "Under Weight"
    elif bmi >= 18.5 and bmi < 24.9:
        return "Normal"
    else:
        return "Overweight"
    

def create_dummy_data():
    template = {
        "Patient_id": None,
        "Patient_Name": None,
        "Patient_detail": {
            "First_Name": None,
            "Middle_Name": None,
            "Last_Name": None,
            "Weight": None,
            "Height": None,
            "Age": None,
            "Address": None,
            "Disease": None,
            "Prescription": None,
            "Medicine": None,
            "Time": None,
        }
    }

    first_names = ["Ankit", "Rahul", "Neha", "Aditi", "Rohit"]
    middle_names = ["Kumar", "Singh", "Prasad", ""]
    last_names = ["Sharma", "Verma", "Patel", "Gupta"]
    diseases = ["Flu", "Diabetes", "Hypertension", "Cold", "Asthma"]
    medicines = ["Paracetamol", "Insulin", "Metformin", "Amlodipine"]
    addresses = ["Delhi", "Mumbai", "Pune", "Chandigarh", "Bangalore"]

    num_patient = 10
    data = {}

    for i in range(1, num_patient + 1):
        patient = json.loads(json.dumps(template))  # deep copy

        first = random.choice(first_names)
        middle = random.choice(middle_names)
        last = random.choice(last_names)

        patient["Patient_id"] = i
        patient["Patient_Name"] = f"{first} {middle} {last}".strip()

        patient["Patient_detail"]["First_Name"] = first
        patient["Patient_detail"]["Middle_Name"] = middle
        patient["Patient_detail"]["Last_Name"] = last
        patient["Patient_detail"]["Weight"] = random.randint(45, 90)
        patient["Patient_detail"]["Height"] = random.randint(150, 190)
        patient["Patient_detail"]["Age"] = random.randint(18, 80)
        patient["Patient_detail"]["Address"] = random.choice(addresses)
        patient["Patient_detail"]["Disease"] = random.choice(diseases)
        patient["Patient_detail"]["Prescription"] = "Take medicine after meals"
        patient["Patient_detail"]["Medicine"] = random.choice(medicines)
        patient["Patient_detail"]["Time"] = random.choice(["Morning", "Afternoon", "Night"])
        patient["Patient_detail"]["BMI"] = bmi(patient["Patient_detail"]['Weight'] , patient["Patient_detail"]['Height'])
        patient["Patient_detail"]["Verdict"] = verdict(patient["Patient_detail"]["BMI"])
        data[f"Patient_{i}"] = patient

    return data


# Example usage
dummy_data = create_dummy_data()

# Print data
print(json.dumps(dummy_data, indent=4))

# Save to file (optional)
with open("patients.json", "w") as f:
    json.dump(dummy_data, f, indent=4)
