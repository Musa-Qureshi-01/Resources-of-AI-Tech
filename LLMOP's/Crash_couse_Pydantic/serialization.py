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

temp  = patient1.model_dump(exclude={'age', 'gender'})

print(temp)
print(type(temp))

temp2  = patient1.model_dump_json(include={'name'})

print(temp2)
print(type(temp2))