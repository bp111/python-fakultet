import pandas as pd
import threading
from src.preprocess import preprocess_data
from src.models import train_logistic_regression, train_knn, train_svm, train_random_forest, train_neural_network
from src.evaluate import evaluate_model, plot_learning_curve

def run_project(cancel_event):    
    yield "Loading dataset...\n"
    filepath = "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        yield f"Error: File {filepath} not found.\n"
        return

    if cancel_event.is_set(): yield "Pipeline Cancelled.\n"; return

    # Preprocess (Collect yielded strings, capture the data tuple)
    data = None
    for msg in preprocess_data(df, cancel_event):
        if isinstance(msg, tuple) and msg[0] == "DATA":
            data = msg[1]
        else:
            yield msg
            
    if cancel_event.is_set(): yield "Pipeline Cancelled.\n"; return
    if not data: return
    
    X_train, X_test, y_train, y_test, scaler, pca = data

    # For learning curve cross-validation
    X_full_train = X_train
    y_full_train = y_train
    
    model_funcs = {
        "Logistic Regression": train_logistic_regression,
        "K-Nearest Neighbors": train_knn,
        "Support Vector Machine": train_svm,
        "Random Forest": train_random_forest,
        "Neural Network": train_neural_network
    }

    # Model training (Collect yields, store the trained model tuples)
    models = {}
    for name, func in model_funcs.items():
        if cancel_event.is_set(): yield "Pipeline Cancelled.\n"; return
        for msg in func(X_train, y_train, cancel_event):
            if isinstance(msg, tuple) and msg[0] == "MODEL":
                models[name] = msg[1]
            else:
                yield msg

    # Evaluation and comparison
    for name, model in models.items():        
        if cancel_event.is_set(): yield "Pipeline Cancelled.\n"; return
        for msg in evaluate_model(name, model, X_test, y_test, cancel_event): 
            yield msg
        for msg in plot_learning_curve(model, name, X_full_train, y_full_train, cancel_event): 
            yield msg

    if not cancel_event.is_set():
        yield "\n*** ML Pipeline Completed Successfully! ***\n"

if __name__ == "__main__":
    # Fallback to test headless script directly
    for output in run_project(threading.Event()):
        if isinstance(output, str) and not output.startswith("IMAGE:"):
            print(output, end="")