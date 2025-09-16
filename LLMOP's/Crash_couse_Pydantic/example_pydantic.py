from pydantic import BaseModel, EmailStr , AnyUrl, Field
from typing import List, Dict,Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length = 30, title= 'Name of the patient', description= 'Give the name of the patient under 30 characters.', examples=['Musa Qureshi', 'Salaar'])]
    age:int = Field(gt=16, lt=80)
    email: EmailStr
    linkedIn_url: AnyUrl
    weight: float = Field(gt=25, lt=200)
    married: bool
    alergies: Optional[List[str]] =  Field(default=None, max_length=5)
    contact: Dict[str, str]

def insert_patient(patient:Patient):

    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedIn_url)
    print(patient.weight)
    print(patient.married)
    print(patient.alergies)
    print(patient.contact)
    print('Patient Data is Inserted.')

patient_info = {'name':'Musa', 'age':19,'email':'musa@gmail.com', 'linkedIn_url':'https://linkedin.com/Musa-Qureshi', 'weight':55, 'married':False, 'alergies':['Girls','Dust','Smoke','pollen'], 'contact':{'email':'musa@gmail.com', 'phone':'6263473208'}}

patient1 = Patient(**patient_info)

insert_patient(patient1)