from fastapi import FastAPI,HTTPException,Path,Query
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
def view_patient(patient_id: str = Path(...,description='ID of the patient in DB',examples='p001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail='patient not found')
    
@app.get('/sort')
def sort_patients(sort_by : str = Query(...,description="chose height ,weight or bmi"), 
                  order : str = Query("asc",description="sort in asc or dsc")
                  ):
    
    valid_fields = ["height","weight","bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400)
    
    if order not in ['asc','dsc']:
        raise HTTPException(status_code=400)
    
    data = load_data()

    sort_order = True if order == 'dsc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)
    return sorted_data
