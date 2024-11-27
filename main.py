from fastapi import FastAPI, HTTPException
from model.pydantic_model import DiabetesInput,DiabetesOutput,DiabetesPrediction,DiabetesPredictionInput
from model.sql_model import Diabetes
from connection import session
from pydantic import BaseModel
import logging
import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
logging.basicConfig(level=logging.ERROR)



app = FastAPI()

#Load the trained model 
try: 
    model = joblib.load("random_forest_model.pkl")
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    raise RuntimeError(f"Error Loading model or scaler: {str(e)}")


@app.post("/diabetes/",response_model=DiabetesOutput)
def create_record(record: DiabetesInput):
    db_session = session()
    db_record = Diabetes(**record.dict())
    db_session.add(db_record)
    db_session.commit()
    db_session.refresh(db_record)
    db_session.close()
    return db_record


@app.get("/getall_diabetes/",response_model=list[DiabetesOutput])
def get_all():
    db_session = session()
    try:
        record = db_session.query(Diabetes).all()
        return record
    finally:
        db_session.close()

@app.get("/diabetes/{id}", response_model=DiabetesOutput)
def read_record(id:int):
    db_session = session()
    try:
        record = db_session.query(Diabetes).filter(Diabetes.id== id).first()
   
        if not record:
            raise HTTPException(status_code = 404, detail = 'Record not found')
        return record
    except Exception as e:
        logging.error(f'Error reading record {e}')
        raise HTTPException(status_code=500,detail=f"Error reading record: {str(e)}")
    
    finally:
        db_session.close()


@app.put("/diabetes/{id}", response_model=DiabetesOutput)
def update_record(id:int,updated_record: DiabetesInput):
    db_session = session()
    record = db_session.query(Diabetes).filter(Diabetes.id==id).first()
    if not record:
        db_session.close()
        raise HTTPException(status_code=404, detail="Record not found")
    
    for key, value in updated_record.dict().items():
        setattr(record,key,value)
    db_session.commit()
    db_session.refresh(record)
    db_session.close()
    return record

@app.delete("/diabetes/{id}",response_model=dict)
def delete_record(id:int):
    db_session = session()
    record = db_session.query(Diabetes).filter(Diabetes.id==id).first()
    if not record:
        db_session.close()
        raise HTTPException(status_code=404, detail="Record Not Found")
    
    db_session.delete(record)
    db_session.commit()
    db_session.close()
    return {"msd":"Record deleted successfully"}

@app.post("/predict_and_save/", response_model=DiabetesOutput)
def predict_and_save(record: DiabetesPredictionInput):
    try:
        #validate
        if record.Gender == 1 and record.Pregnancies !=0:
            raise HTTPException(
                status_code=400,
                detail="Invalid data: Pregnencies must be 0 for males"
            )
        # Prepare the input data for prediction
        data = {
            
            "Gender": [record.Gender],
            "Age": [record.Age],
            "Pregnancies": [record.Pregnancies],
            "Glucose": [record.Glucose],
            "BloodPressure": [record.BloodPressure],
            "SkinThickness": [record.SkinThickness],
            "Insulin": [record.Insulin],
            "BMI": [record.BMI],
            "DiabetesPedigreeFunction": [record.DiabetesPedigreeFunction]
        }

        data["Glucose_Insulin"]= [record.Glucose* record.Insulin]
        data["BMI_Age"] = [record.BMI * record.Age]
        df = pd.DataFrame(data)

        df["id"] = [0]

        ordered_columns = [
            'Gender', 'Age', 'Pregnancies', 'Glucose', 'BloodPressure',
            'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
            'Glucose_Insulin', 'BMI_Age'
        ]

        df = df[ordered_columns]


        # Scale the input data using the loaded scaler
        data_scaled = scaler.transform(df)

        # Make the prediction
        prediction = model.predict(data_scaled)
        outcome = 1 if prediction[0] == 1 else 0

        # Save the input data along with the prediction to the database
        db_session = session()
        db_record = Diabetes(
            Gender=record.Gender,
            Age = record.Age,
            Pregnancies=record.Pregnancies,
            Glucose=record.Glucose,
            BloodPressure=record.BloodPressure,
            SkinThickness=record.SkinThickness,
            Insulin=record.Insulin,
            BMI=record.BMI,
            DiabetesPedigreeFunction=record.DiabetesPedigreeFunction,
            
            Outcome=outcome  # Store prediction result in Outcome
        )
        db_session.add(db_record)
        db_session.commit()
        db_session.refresh(db_record)

        # Return the saved record and prediction result
        return db_record
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Error during prediction and saving: {str(e)}")
    
    finally:
        db_session.close()