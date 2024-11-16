
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataCleaning.data_cleaning import clean_data
from model.sql_model import Base,Diabetes

db_user:str = 'postgres'
db_port:int = 5432
db_host:str = 'localhost'
db_password:str = '1234'
uri:str = f'postgresql+pg8000://{db_user}:{db_password}@{db_host}:{db_port}/diabetes'



engine = create_engine(uri)


# df = pd.read_csv('diabetes.csv')
# print(df.head())



session = sessionmaker(
    bind=engine,
    autoflush=True

)
db_session = session()

Base.metadata.create_all(engine)

try:




    filepath = 'diabetes.csv'
    cleaned_data = clean_data(filepath)
    cleaned_data.to_sql('diabetes_dataset',engine,if_exists='replace',index=False)
    print("Cleaned data loaded into the database successfully")    

except Exception as e:
    print(f"{e}")


finally:
    db_session.close()

