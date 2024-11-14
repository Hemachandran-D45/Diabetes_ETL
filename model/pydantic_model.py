from pydantic import BaseModel

class DiabetesInput(BaseModel):
    Pregnancies: int
    Glucose : float
    Blood_Pressure: float
    Skin_Thickness:float
    Insulin : float
    BMI : float
    Diabetes_Pedigree_Fuction : float
    Age : int
    Outcome : int


class DiabetesOutput(DiabetesInput):
    id : int

    class Config:
        orm_model = True