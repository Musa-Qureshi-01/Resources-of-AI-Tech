from pydantic import BaseModel, Field
from typing import Optional
from pydantic.networks import EmailStr

class Student(BaseModel):
    name: str = "Musa"
    age: Optional[int] = Field(default=None, description="Age of the student")
    email: EmailStr
    cgpa: float = Field(ge=0.0, le=9.0, default=7.5, description="CGPA of the student")  # fixed default

new_student = {'age': 19, 'email': 'musaqureshi0a@gmail.com'}

student = Student(**new_student)

student_dict = dict(student)

print(student_dict)

student_json = student.model_dump_json()
