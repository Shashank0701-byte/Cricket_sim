import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

from app.ml.feature_extractor import extract_raw_deliveries, build_features

def train_model():
    print("Extracting data from database...")
    df = extract_raw_deliveries()
    
    if len(df) == 0:
        print("No data found in database. Please run ingestion first.")
        return
        
    print(f"Loaded {len(df)} deliveries. Building features...")
    X, y = build_features(df)
    
    # Encode target labels
    le_y = LabelEncoder()
    y_encoded = le_y.fit_transform(y)
    
    # Encode categorical features (batter_id, bowler_id)
    # We must save these encoders to use them during simulation!
    le_batter = LabelEncoder()
    le_bowler = LabelEncoder()
    
    X_encoded = X.copy()
    X_encoded['batter_id'] = le_batter.fit_transform(X['batter_id'])
    X_encoded['bowler_id'] = le_bowler.fit_transform(X['bowler_id'])
    
    # Split chronologically
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42, shuffle=False)
    
    print(f"Training XGBoost Classifier on {len(X_train)} samples...")
    # Outcomes: 0-6 runs, 7 Wicket, 8 Extra (so 9 classes total potentially)
    model = xgb.XGBClassifier(
        objective='multi:softprob',
        num_class=9,
        eval_metric='mlogloss',
        use_label_encoder=False,
        tree_method='hist'
    )
    
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    # Save model and encoders
    model_dir = Path(os.path.dirname(__file__)) / "models"
    model_dir.mkdir(exist_ok=True)
    
    joblib.dump(model, model_dir / "ball_simulator_v1.joblib")
    joblib.dump(le_y, model_dir / "label_encoder_y.joblib")
    joblib.dump(le_batter, model_dir / "label_encoder_batter.joblib")
    joblib.dump(le_bowler, model_dir / "label_encoder_bowler.joblib")
    print(f"Model and encoders saved successfully to {model_dir}")

if __name__ == "__main__":
    train_model()
