
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataCleaning.data_cleaning import clean_data
from model.sql_model import Base,Diabetes
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="venv\Lib\site-packages\python_dotenv-1.0.1.dist-info\.env")

db_user = os.getenv('DB_USER')
db_password= os.getenv('DB_PASSWORD')
db_port:int = 5432
db_host:str = 'localhost'
uri:str = f'postgresql+pg8000://{db_user}:{db_password}@{db_host}:{db_port}/diabetes'


engine = create_engine(uri)


# df = pd.read_csv('diabetes.csv')
# print(df.head())



session = sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=False

)
db_session = session()
Base.metadata.drop_all(engine)  # This will drop the existing table
Base.metadata.create_all(engine)

try:

    filepath = 'diabetes.csv'
    cleaned_data = clean_data(filepath)
    if 'id' in cleaned_data.columns:
        cleaned_data = cleaned_data.drop(columns=['id'])

    # Check for existing data and add only new records
    existing_ids = {row.id for row in db_session.query(Diabetes.id).all()}
    new_data = cleaned_data[~cleaned_data.index.isin(existing_ids)]

    if not new_data.empty:
        new_data.to_sql('diabetes', engine, if_exists='append', index=False)
        print(f"{len(new_data)} new rows added to the database.")
    else:
        print("No new data to load.")
   


except Exception as e:
    print(f"{e}")


finally:
    db_session.close()

