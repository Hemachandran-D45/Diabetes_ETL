from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,Float

Base = declarative_base()

class Diabetes(Base):
    __tablename__ = 'diabetes_dataset'
    id = Column(Integer, primary_key=True, index=True)
    Pregnancies = Column(Integer)
    Glucose = Column(Float)
    BloodPressure = Column(Float)
    SkinThickness = Column(Float)
    Insulin =  Column(Float)
    BMI = Column(Float)
    DiabetesPedigreeFunction = Column(Float)
    Age = Column(Integer)
    Outcome = Column(Integer)   