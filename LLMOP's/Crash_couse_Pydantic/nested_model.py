from pydantic import BaseModel, EmailStr , AnyUrl, Field
from typing import List, Dict,Optional, Annotated

class Address(BaseModel):
    city:str
    state:str
    pin:int

class Patient(BaseModel):
    name:str
    gender: str
    age :int
    address: Address

address_dict = {'city':'bhopal', 'state':'male', 'pin':462001}

address1 = Address(**address_dict)

patient_dict =  {'name':'Musa', 'gender':'male', 'age':19, 'address':address1}

patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.pin)