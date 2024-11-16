from fastapi import FastAPI, HTTPException
from model.pydantic_model import DiabetesInput,DiabetesOutput
from model.sql_model import Diabetes
from connection import session
import logging

logging.basicConfig(level=logging.ERROR)



app = FastAPI()

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
