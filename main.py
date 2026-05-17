from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import json
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(...,description="ID of the patient")]
    name : Annotated[str, Field(...,description="Name of the patient")]
    city : Annotated[str, Field(...,description="City of the patient")]
    age : Annotated[int, Field(...,gt=0,lt=120,description="Age of the patient")]
    gender : Annotated[Literal['male','female','others'], Field(...,description="Gender of the patient")]
    height : Annotated[float, Field(...,description="Height of the patient")]
    weight : Annotated[float, Field(...,description="Weight of the patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 25:
            return "normal"
        elif self.bmi < 30:
            return "normal"
        else:
            return "obese"    

def load_data():
    with open("patients.json",'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data, f)



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

@app.post('/create')
def create_patient(patient:Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="already exists")
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})






