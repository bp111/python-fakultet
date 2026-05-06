import pandas as pd
from src.preprocess import preprocess_data
from src.models import train_logistic_regression, train_knn, train_svm, train_random_forest, train_neural_network
from src.evaluate import evaluate_model, plot_learning_curve

def run_project():    
    filepath = "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    df = pd.read_csv(filepath)
        
    X_train, X_test, y_train, y_test, scaler, pca = preprocess_data(df)
    
    # For learning curve cross-validation
    X_full_train = X_train
    y_full_train = y_train

    # Model training
    models = {
        "Logistic Regression": train_logistic_regression(X_train, y_train),
        "K-Nearest Neighbors": train_knn(X_train, y_train),
        "Support Vector Machine": train_svm(X_train, y_train),
        "Random Forest": train_random_forest(X_train, y_train),
        "Neural Network": train_neural_network(X_train, y_train)
    }

    # Evaluation, comparison
    for name, model in models.items():        
        evaluate_model(name, model, X_test, y_test) # Printing metrics, confusion matrix
                
        plot_learning_curve(model, name, X_full_train, y_full_train)

if __name__ == "__main__":
    run_project()