import os
import matplotlib
matplotlib.use('Agg') # For generating plots safely in a Flask thread
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import learning_curve
import numpy as np

def evaluate_model(model_name, model, X_test, y_test, cancel_event):
    if cancel_event.is_set(): return
    yield f"\n{'='*40}\n--- Evaluation for {model_name} ---\n{'='*40}\n"
    
    # Make predictions
    y_pred = model.predict(X_test)
        
    yield f"Accuracy: {accuracy_score(y_test, y_pred):.4f}\n\n"
    yield "Classification Report:\n" # (F1-Score, Precision, Recall)
    yield classification_report(y_test, y_pred) + "\n"
    
    # Confusion matrix visualization
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title(f'Confusion Matrix: {model_name}')
    plt.xlabel('Predicted Label (0=No Churn, 1=Churn)')
    plt.ylabel('True Label')
    plt.tight_layout()
    # Save the figure instead of plt.show()
    os.makedirs('static/images', exist_ok=True)
    filepath = f"static/images/cm_{model_name.replace(' ', '_')}.png"
    plt.savefig(filepath)
    plt.close()
    
    yield f"IMAGE:/{filepath}\n"

def plot_learning_curve(estimator, title, X, y, cancel_event, cv=5):
    if cancel_event.is_set(): return
    yield f"Generating learning curve for {title}...\n"
    
    plt.figure(figsize=(8, 5))
    plt.title(f"Learning Curve: {title}")
    plt.xlabel("Training Examples")
    plt.ylabel("F1 Score")

    # Calculate learning curve metrics
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=-1, 
        train_sizes=np.linspace(0.1, 1.0, 5), scoring='f1'
    )

    # Calculate mean and standard deviation
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.grid()
    # Plot the bands for variance
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std, 
                     train_scores_mean + train_scores_std, alpha=0.1, color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std, 
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")

    # Plot the actual lines
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")

    plt.legend(loc="best")
    plt.tight_layout()    
    # Save the figure
    filepath = f"static/images/lc_{title.replace(' ', '_')}.png"
    plt.savefig(filepath)
    plt.close()
    
    yield f"IMAGE:/{filepath}\n"