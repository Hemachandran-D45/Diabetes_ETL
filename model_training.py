import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, ConfusionMatrixDisplay
from Eda import load_cleaned_data, detect_outlier
from feature_engineering import feature_engineering
import matplotlib.pyplot as plt 
import joblib



def train_and_evaluate_model():
    #Load and preprocess data
    table_name = "diabetes_dataset"
    data = load_cleaned_data(table_name)

    if not data.empty:
        #Handle outliers and perform feature engineering
        #Removing or managing outliers ensure the model is not biased by extreme value
        data = detect_outlier(data)
        #Feature engineering enchanced the model's ability to identify patterns in the data 
        engineering_data = feature_engineering(data)

        #Prepare the data for training
        X = engineering_data.drop(columns=['id','Outcome','Age_Bin','BMI_Category'])
        y = engineering_data['Outcome']
        print(X.columns)
        print(y)

        #Split into training(80%) and testing data(20%)
        #train_test_split shuffles the data and splits it into random subsets

        X_train,X_test,y_train,y_test = train_test_split( X,y,test_size=0.2, random_state=42)

        #scale the data 
        #**StandardScaler** is used to scale the range of independent variables so can be comapred more easily
        #fit_transform is used on training data to learn the paramters like mean, sd and scale it
        #transform is the used to the test data to sclae it using parametes learned from the training data 
        scaler = StandardScaler()
        
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        #Train the model
        #Model 1: Random Forest Classifier : is an ensemble method that uses multiple decision tress to make decision

        rf_model = RandomForestClassifier(random_state=42)
        rf_model.fit(X_train_scaled,y_train)
        #save the random forest model and scaler
        joblib.dump(rf_model,"random_forest_model.pkl")
        joblib.dump(scaler,"scaler.pkl")
        print("Random Forest model and scaler saved successfully")
        print("\n=== Random Forest Classifier ===")
        
        #Make prediction with Random forest
        rf_y_pred = rf_model.predict(X_test_scaled)
    
        #Evaluate the model
        print("Accuracy:", accuracy_score(y_test,rf_y_pred))
        print("Classification Report:") 
        print(classification_report(y_test,rf_y_pred)) #provides precision, recall, f1-score for each class


        #COnfusion Matrix  : shows the number of correct and incorrect prediction 
        cm = confusion_matrix(y_test,rf_y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Diabetes","Diabetes"])
        disp.plot(cmap="Blues") 
        plt.show()
        #Model 2: Logistic Regression
        print("\n=== Logistic Regression===")
        lr_model = LogisticRegression(random_state=42, max_iter=1000)
        lr_model.fit(X_train_scaled,y_train)

        #Make prediction with LR is a linearn model for binary classification
        lr_y_pred = lr_model.predict(X_test_scaled)

        #Evaluate LR
        print("Accuracy:" , accuracy_score(y_test,lr_y_pred))
        print("Classification Report:")
        print(classification_report(y_test, lr_y_pred))




        #Compare real vs predicted
        comparision_df = pd.DataFrame({
            'Real Outcome': y_test.values,
            'RF Predicted':rf_y_pred,
            'Logistics Regression Predicted':lr_y_pred})
        print("\nCOmparision of Real vs Predicted Outcomes:")
        print(comparision_df.head(20))

    else:
        print("No data available for model training")

if __name__ == "__main__":
    train_and_evaluate_model()





'''
Summary:
    Load Data
    Preprocess 
    Split Data
    Scale Data
    Train model
    Evaluate model 

Metrics Explanation:

1. **Accuracy**  
   The ratio of correctly predicted observations to the total observations.  
   Accuracy is a simple and useful metric, but it can be misleading if the dataset is imbalanced (e.g., if most cases are negative).

2. **Precision**  
   The ratio of correctly predicted positive observations to the total predicted positive observations.  
   - Precision minimizes false positives (FP).  
   - Example: In spam detection, you want to ensure legitimate emails aren't wrongly marked as spam.

3. **Recall (Sensitivity or True Positive Rate)**  
   The ratio of correctly predicted positive observations to all actual positive observations.  
   - High recall ensures fewer false negatives.  
   - Example: In diabetes prediction, you want to detect as many true diabetes cases as possible.

4. **F1-Score**  
   The harmonic mean of precision and recall.  
   F1-score balances precision and recall, useful when both are important.  
   - Example: In medical diagnostics, both missing true cases (false negatives) and wrongly classifying healthy people (false positives) are harmful.

Key Terms Explained:

- **Random State**:  
  Random state is a parameter used in various functions like `train_test_split` and models to ensure the results are reproducible. 
  If you set the same random state number, you will get the same random split or results each time the code is run, which is useful for consistency and debugging.

- **StandardScaler**:  
  StandardScaler standardizes the data by removing the mean and scaling it to unit variance. 
  This helps improve the performance and convergence speed of the model, especially for models sensitive to feature scaling like Logistic Regression.

- **fit_transform**:  
  This method is used to both "fit" the scaler to the training data (learn the mean and standard deviation) and then "transform" the data by scaling it. 
  This is done only on the training set.

- **transform**:  
  This method is used to transform the test set using the parameters (mean and standard deviation) learned from the training data. 
  It is crucial to avoid data leakage, where the test set influences the model during training.

- **Confusion Matrix**:  
  A confusion matrix helps evaluate the performance of a classification model. It shows the number of correct and incorrect predictions for each class (e.g., diabetes vs. no diabetes).
  The matrix gives insights into precision, recall, and overall accuracy.

- **max_iter**:  
  In Logistic Regression, `max_iter` specifies the maximum number of iterations the solver should run before stopping.
  Increasing it can help achieve convergence when the model isn't fully converging within the default number of iterations.

'''

     
