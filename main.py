from fastapi import FastAPI,HTTPException,Path
import json
app = FastAPI()

def load_data():
    with open("patients.json",'r') as f:
        data = json.load(f)

    return data

@app.get("/")
def hello():
    return{'message' : "Patient Management System API"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get('/patient_id/{patient_id}')
def view_patient(patient_id: str = Path(...,description='ID of the patient in DB',example='p001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail='patient not found')