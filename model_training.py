import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, ConfusionMatrixDisplay
from Eda import load_cleaned_data, detect_outlier
from feature_engineering import feature_engineering



def train_and_evaluate_model():
    #Load and preprocess data
    table_name = "diabetes_dataset"
    data = load_cleaned_data(table_name)

    if not data.empty:
        #Handle outliers and perform feature engineering

        data = detect_outlier(data)
        engineering_data = feature_engineering(data)

        #Prepare the data for training
        X = engineering_data.drop(columns=['Outcome','Age_Bin','BMI_Category'])
        y = engineering_data['Outcome']

        #Split into training and testing data
        X_train,X_test,y_train,y_test = train_test_split( X,y,test_size=0.2, random_state=45)

        #scale the data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        #Train the model
        model = RandomForestClassifier(random_state=45)
        model.fit(X_train_scaled,y_train)

        #Make prediction 
        y_pred = model.predict(X_test_scaled)

        #Evaluate the model
        print("Accuracy:", accuracy_score(y_test,y_pred))
        print("Classification Report:") 
        print(classification_report(y_test,y_pred))

        #COnfusion Matrix 
        cm = confusion_matrix(y_test,y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Diabetes","Diabetes"])
        disp.plot(cmap="Blues") 

        #Compare real vs predicted
        comparision_df = pd.DataFrame({'Real Outcome': y_test.values,'Predicted Outcome':y_pred})
        print(comparision_df.head(20))

    else:
        print("No data available for model training")

if __name__ == "__main__":
    train_and_evaluate_model()

     
