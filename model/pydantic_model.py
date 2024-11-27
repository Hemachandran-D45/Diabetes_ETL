from pydantic import BaseModel, Field, model_validator, ValidationError

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


class DiabetesPredictionInput(BaseModel):
    
    Age:int
    Gender:int
    Pregnancies: int
    Glucose : float
    BloodPressure: float
    SkinThickness:float
    Insulin : float
    BMI : float
    DiabetesPedigreeFunction : float
   
    @model_validator(mode="before")
    def check_valid_data(cls, values):
        # Ensure Gender is either 0 (Female) or 1 (Male)
        if values.get('Gender') not in [0, 1]:
            raise ValueError("Gender must be 0 (Female) or 1 (Male)")
        
        # Ensure Pregnancies is 0 for males (Gender = 1)
        if values.get('Gender') == 1 and values.get('Pregnancies') != 0:
            raise ValueError("Pregnancies must be 0 for males (Gender = 1)")
        
        # Ensure Pregnancies is a non-negative value for females (Gender = 0)
        if values.get('Gender') == 0 and values.get('Pregnancies') < 0:
            raise ValueError("Pregnancies must be a non-negative value for females (Gender = 0)")
        
        return values



class DiabetesPrediction(BaseModel):
    prediction: str
