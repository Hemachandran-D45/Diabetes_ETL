from pydantic import BaseModel

class DiabetesInput(BaseModel):
    id : int
    Pregnancies: int
    Glucose : float
    BloodPressure: float
    SkinThickness:float
    Insulin : float
    BMI : float
    DiabetesPedigreeFunction : float
    Age : int
    Outcome : int


class DiabetesOutput(DiabetesInput):
    id : int

    class Config:
        from_attributes = True