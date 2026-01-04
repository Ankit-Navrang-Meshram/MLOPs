from fastapi import FastAPI , Path , HTTPException , Query
import json


def load_data():
    with open("patients.json" ,'r') as f:
        data = json.load(f)
    return data

app = FastAPI()

@app.get('/')
def intro():
    return "Welcome to Apna Hospital !!!"

@app.get('/about')
def info():
    return "This API helps you to interact with paitents data."

@app.get("/view")
def get_patientsw_data():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_patient_by_id(patient_id: int = Path(... , description = "This is patient ID, it is an integer value ..." , example = 1 , gt = 0)):
    data = load_data()
    patient_key = f"Patient_{patient_id}"
    if patient_key in data:
        return data[patient_key]
    else:
        # return {"error": "Patient not found"} instead we will return a 404 error 
        return HTTPException(status_code=404 , detail = "Patient not found")
    
@app.get("/patient/sort")
def sort_patients(age : int = Query(... , description = "Age to filter patients older than this age" , example = 30 , gt = 0), height : int = Query(None, description = "Height to filter patients taller than this height" , example = 170) , weight : int = Query(None , description = "Weight to filter paitents heavier than this weight" , example = 70) , order_by : str = Query("acs" , description = "Order by ascending or descending, default is ascending" , example = "desc")):
    data = load_data()
    filtered_patients = []

    for patient_key, patient_info in data.items():
        patient_detail = patient_info["Patient_detail"]
        if patient_detail["Age"] > age:
            if height is not None and patient_detail["Height"] <= height:
                continue
            if weight is not None and patient_detail["Weight"] <= weight:
                continue
            filtered_patients.append(patient_info)

    reverse_order = True if order_by == "desc" else False
    sorted_patients = sorted(filtered_patients, key=lambda x: x["Patient_detail"]["Age"], reverse=reverse_order)

    return sorted_patients
