import pandas as pd 
import numpy as np
from Perform.Eda import load_cleaned_data, detect_outlier

def create_age_bins(df:pd.DataFrame) -> pd.DataFrame:
    """Create age bins and add new column"""
    bins = [20,30,40,50,60,70,80,90]
    labels = ['20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
    df['Age_Bin'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    return df

def group_bmi(df:pd.DataFrame) -> pd.DataFrame:
    bins = [0,18.5, 24.9, 29.9, 34.9]
    labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
    df["BMI_Category"] = pd.cut(df['BMI'],bins=bins,labels=labels,right=False)
    return df

def create_interaction_terms(df:pd.DataFrame)->pd.DataFrame:
    """Xreate interaction terms between features."""
    df['Glucose_Insulin'] = df['Glucose']*df['Insulin']
    df["BMI_Age"] = df["BMI"] * df["Age"]
    return df

def feature_engineering(df:pd.DataFrame) ->pd.DataFrame:
    """Perform all feature engineering steps"""
    df= create_age_bins(df)
    df = group_bmi(df)
    df=create_interaction_terms(df)
    return df

if __name__ == '__main__':
    #load the cleaned data 
    table_name = 'diabetes'

    data = load_cleaned_data(table_name)
    if not data.empty:
        #Ensure the data is cleaned before feature engineering
        data = detect_outlier(data)
        engineered_data = feature_engineering(data)
        print(engineered_data.head())
        

    else :
        print("No Data available for feature engineering")