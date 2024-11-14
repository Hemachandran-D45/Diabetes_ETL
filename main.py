from fastapi import FastAPI, HTTPException
from model.pydantic_model import DiabetesInput,DiabetesOutput
from model.sql_model import Diabetes
from connection import session
app = FastAPI()

@app.post("/diabetes/",response_model=DiabetesOutput)
def create_record(record: DiabetesInput):
    db_session = session()
    db_record = Diabetes(**record.dict())
    db_session.add(db_record)
    db_session.refresh(db_record)
    db_session.close()
    return db_record


@app.get("/diabetes/{id}", response_model=DiabetesOutput)
def read_record(id:int):
    db_session = session()
    try:
        record = db_session.query(Diabetes).filter(Diabetes.id == id).first()
   
        if not record:
            raise HTTPException(status_code = 404, detail = 'Record not found')
        return record
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error reading record: {str(e)}")
    
    finally:
        db_session.close()