from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

def train_logistic_regression(X_train, y_train):
    print("\nTraining Logistic Regression with GridSearchCV...")
    
    # Model
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    
    # Hyperparameters to test
    param_grid = {
        'C': [0.01, 0.1, 1, 10, 100], 
        'solver': ['lbfgs', 'liblinear']
    }
        
    # Score based on 'f1' because this particular dataset is imbalanced
    grid = GridSearchCV(log_reg, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    print(f"Best LR Parameters found: {grid.best_params_}")
    return grid.best_estimator_

def train_knn(X_train, y_train):
    print("\nTraining K-Nearest Neighbors with GridSearchCV...")
    
    knn = KNeighborsClassifier()
    
    # Hyperparameters: number of neighbors (k), weight type, and distance metric (p)
    param_grid = {
        'n_neighbors': [3, 5, 7, 9, 11, 15],
        'weights': ['uniform', 'distance'],
        'p': [1, 2] # 1 = Manhattan distance, 2 = Euclidean distance
    }
    
    grid = GridSearchCV(knn, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    print(f"Best KNN Parameters found: {grid.best_params_}")
    return grid.best_estimator_

def train_svm(X_train, y_train):
    print("\nTraining Support Vector Machine (SVM) with GridSearchCV...")
    
    # probability=True allows us to use predict_proba later if we want ROC curves
    svm = SVC(probability=True, random_state=42)
    
    param_grid = {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf'], # rbf - Radial Basis Function
        'gamma': ['scale', 'auto']
    }
    
    grid = GridSearchCV(svm, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    print(f"Best SVM Parameters found: {grid.best_params_}")
    return grid.best_estimator_

def train_random_forest(X_train, y_train):
    print("\nTraining Random Forest with GridSearchCV...")
    
    rf = RandomForestClassifier(random_state=42)
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 5, 10, 20],
        'min_samples_split': [2, 5]
    }
    
    grid = GridSearchCV(rf, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    print(f"Best Random Forest Parameters found: {grid.best_params_}")
    return grid.best_estimator_

def train_neural_network(X_train, y_train):
    print("\nTraining Neural Network (MLP) with GridSearchCV...")
    
    # max_iter is high to ensure the network has time to converge
    nn = MLPClassifier(max_iter=1500, random_state=42)
    
    param_grid = {
        'hidden_layer_sizes': [(50,), (100,), (50, 50)], # 1 or 2 hidden layers
        'activation': ['relu', 'tanh'],
        'learning_rate_init': [0.001, 0.01]
    }
    
    grid = GridSearchCV(nn, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    print(f"Best Neural Network Parameters found: {grid.best_params_}")
    return grid.best_estimator_