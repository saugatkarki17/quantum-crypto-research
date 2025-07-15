import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
import joblib
import os
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

def train_anomaly_detection_model(dataset_path='results/kyber_dataset.csv'):
    # Load dataset
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"No dataset at {dataset_path}. Run kyber_dataset_generator.py first!")
        return

    # Prep data
    features = ['plaintext_length', 'key_size', 'ciphertext_size', 'encrypt_time', 'decrypt_time', 'cpu_load_duration_ms']
    X = df[features]
    y = df['is_anomaly']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    # Save scaler
    scaler_path = os.path.join("ml", "scaler.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")

    # --- Random Forest Classifier ---
    print("\nTraining Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    y_proba_rf = rf_model.predict_proba(X_test)[:, 1]

    print("\nRandom Forest Results:")
    print(classification_report(y_test, y_pred_rf))

    # Confusion Matrix Chart
    cm_rf = confusion_matrix(y_test, y_pred_rf)
    if cm_rf.shape == (2, 2):
        ```chartjs
        {
            "type": "bar",
            "data": {
                "labels": ["Normal", "Anomaly"],
                "datasets": [
                    {
                        "label": "Predicted Normal",
                        "data": [${cm_rf[0][0]}, ${cm_rf[1][0]}],
                        "backgroundColor": "rgba(54, 162, 235, 0.8)"
                    },
                    {
                        "label": "Predicted Anomaly",
                        "data": [${cm_rf[0][1]}, ${cm_rf[1][1]}],
                        "backgroundColor": "rgba(255, 99, 132, 0.8)"
                    }
                ]
            },
            "options": {
                "plugins": { "title": { "display": true, "text": "Random Forest Confusion Matrix" } },
                "scales": {
                    "x": { "title": { "display": true, "text": "Predicted" } },
                    "y": { "title": { "display": true, "text": "Actual" }, "beginAtZero": true }
                }
            }
        }