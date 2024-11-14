import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_user:str = 'postgres'
db_port:int = 5432
db_host:str = 'localhost'
db_password:str = '1234'
uri:str = f'postgresql+pg8000://{db_user}:{db_password}@{db_host}:{db_port}/diabetes'



engine = create_engine(uri)

df = pd.read_csv('diabetes.csv')
# print(df.head())



session = sessionmaker(
    bind=engine,
    autoflush=True

)


try:
    connection = engine.connect()
    connection.close()
    print("Connected")

except Exception as e:
    print(str(e))

df.to_sql('diabetes_dataset',engine,if_exists="replace",index=False)
print("Data loaded into Postgres")