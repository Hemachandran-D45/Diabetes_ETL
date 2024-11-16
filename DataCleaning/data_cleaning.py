import pandas as pd
import numpy as np

def clean_data(filepath:str) -> pd.DataFrame:

    df = pd.read_csv(filepath)
    # count = (df[["Pregnancies"]]==0).sum()
    # print(count)

    np.random.seed(42) 
    #generate random with specific seed (in this case 42) if i run the code multiple times the value in gender column will always be same 
    df["Gender"] = np.random.choice([0,1], size=len(df)) #0,1 randomly in te count of length of the df

    # print(df.head())
    df.loc[df["Gender"]==1, 'Pregnancies'] = 0 #change the pregnancy value for male

    # glu_mean = df['Glucose'].mean()
    # df['Glucose'] = df['Glucose'].replace(0,glu_mean)

    # mean_glu=df['Glucose'].mean()
    # print(mean_glu)
    if id  not in df.columns:
        df['id'] = range(1,len(df)+1)

    column_fix = ['Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction']

    for column in column_fix:
        # first replace zero with nan to calculate median then with median
        median_value = df[column].replace(0,pd.NA).median()
        df[column] = df[column].replace(0,median_value)

    df_loc = ['id','Gender','Age','Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Outcome']
    df = df[df_loc]
    # print(df.head())
    outcome_removed = df.drop(columns=['Outcome'])

    X = outcome_removed
    Y = df['Outcome']

    df_combined = X.copy()
    df_combined['Outcome']= Y
    print(df_combined.head())

    return df_combined

    """
    Cleans the diabetes dataset for modeling:
    
    - Adds a 'Gender' column with random values (0 for female, 1 for male).
    - Sets 'Pregnancies' to 0 for males (Gender = 1).
    - Replaces zero values in specified columns with their respective median values.
    - Rearranges the columns for better readability.
    - Splits the cleaned dataset into features (X) and target (Y).
    
    Parameters:
    - filepath (str): The path to the diabetes dataset CSV file.

    Returns:
    - X (pd.DataFrame): Cleaned dataset features.
    - Y (pd.Series): Target variable ('Outcome').

    """


# filepath = 'diabetes.csv'
# X,Y = clean_data(filepath)
