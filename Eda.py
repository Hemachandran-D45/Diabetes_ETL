import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

db_user:str = "postgres"
db_password:str = '1234'
db_host:str ='localhost'
db_port:int = 5432


uri = f'postgresql+pg8000://{db_user}:{db_password}@{db_host}:{db_port}/diabetes'
engine = create_engine(uri)

def load_cleaned_data(table_name :str)->pd.DataFrame:
    """ Load cleaned data from the specified table in the database"""
    try:
        query = f"Select * from {table_name}"
        df = pd.read_sql_query(query, con=engine)
        return df
    
    except Exception as e:
        print(f"Error loading data : {e}")
        return pd.DataFrame()
    
# def display_min_max_values(df: pd.DataFrame):
#     """Display minimum and maximum values for each column in the dataframe"""
#     min_max_values = pd.DataFrame({
#         'Column': df.columns,
#         'Minimum Value': df.min(),
#         'Maximum Value': df.max()
#     })
#     print(min_max_values)
    

def detect_outlier(df: pd.DataFrame):
    """Detect and handle outlier using IQR method"""
    numeric_columns = df.select_dtypes(include=["float64","int64"]).columns
    numeric_columns = [col for col in numeric_columns if col not in ['id','Outcome']]


    intial_rows = df.shape[0]
    print(f'Initial number of rows : {intial_rows}')

    # min_age = df['Age'].min()
    # max_age = df['Age'].max() 
    # print(f'mini age {min_age}')
    # print(f'max age {max_age}')
    #plot before handlng outliers (boxplot)
    plt.figure(figsize=(12,8))
    for i , col in enumerate(numeric_columns,1):
        
        #create 3x3 grid for boxplot
        plt.subplot(3,3,i)
        sns.boxplot(df[col])
        plt.title(f"Boxplot of {col}")
    plt.tight_layout()
    plt.show()

    #calculate q1,q3, and iqr for each numberical column
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3-Q1 

        #calculate the outlier boundaries
        lower_bound = Q1 - 3.5 * IQR
        upper_bound = Q3 + 3.5 * IQR

        #filter out rows with outliers
        df = df[(df[col] >= lower_bound )&(df[col]<=upper_bound)]
    
    final_rows = df.shape[0]
    print(f'Number of rows after the outlier removal: {final_rows}')
    rows_removed = intial_rows - final_rows
    print(f"Rows removed : { rows_removed}")


    plt.figure(figsize=(12,8))
    for i, col in enumerate(numeric_columns,1):
        plt.subplot(3,3,i)
        sns.boxplot(df[col])
        plt.title(f'Boxplot of {col} After Handling Outliers')
    plt.tight_layout()
    plt.show()
    return df 




def perform_eda(df: pd.DataFrame):
    """Perform Eda on th given Dataframe"""
    print("Basic Information: ")
    print(df.info())
    print("\n Summary Statistics:")
    print(df.describe())

    #checking for missing value
    print("\n Missing Value")
    print(df.isna().sum())

    #exclude id and outcome col from hist
    numeric_columns = df.select_dtypes(include=["float64","int64"]).columns
    numeric_columns = [col for col in numeric_columns if col not in ['id','outcome']]

    for col in numeric_columns:
        plt.figure(figsize=(6,4))
        sns.histplot(df[col], kde=True, bins=30, color='blue')
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.show()
        #plt.savefig(f"{column}_distribution.png")

   

        #colleration heatmap
    plt.figure(figsize=(10,8))
    sns.heatmap(df.corr(),annot=True,cmap='coolwarm',fmt='.2f')
    plt.title("Correlation Matrix")
    plt.show()

    #     #pairplot for numerical col 
    # sns.pairplot(df[numeric_columns])
    # plt.title("Pairplot of Numerical Features")
    # plt.show()


if __name__ == "__main__":

    table_name = 'diabetes_dataset'
    data = load_cleaned_data(table_name)

    if not data.empty:
        # display_min_max_values(data)
        data = detect_outlier(data)
        perform_eda(data)

    else:
        print("No data avaiable for EDA")
