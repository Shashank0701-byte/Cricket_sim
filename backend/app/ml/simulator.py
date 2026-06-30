import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

class MatchSimulator:
    def __init__(self):
        model_dir = Path(os.path.dirname(__file__)) / "models"
        self.model = joblib.load(model_dir / "ball_simulator_v1.joblib")
        self.le_y = joblib.load(model_dir / "label_encoder_y.joblib")
        self.le_batter = joblib.load(model_dir / "label_encoder_batter.joblib")
        self.le_bowler = joblib.load(model_dir / "label_encoder_bowler.joblib")
        
        self.known_batters = set(self.le_batter.classes_)
        self.known_bowlers = set(self.le_bowler.classes_)
        
    def _safe_transform(self, encoder, val, known_set):
        if val in known_set:
            return encoder.transform([val])[0]
        # Fallback to a generic/known player if unseen
        return 0

    def simulate_ball(self, batter_id: str, bowler_id: str, 
                      innings_number: int, over_number: int, 
                      delivery_number: int, innings_runs: int, 
                      innings_wickets: int) -> str:
                      
        batter_encoded = self._safe_transform(self.le_batter, batter_id, self.known_batters)
        bowler_encoded = self._safe_transform(self.le_bowler, bowler_id, self.known_bowlers)
        
        features = pd.DataFrame([{
            'batter_id': batter_encoded,
            'bowler_id': bowler_encoded,
            'innings_number': innings_number,
            'over_number': over_number,
            'delivery_number': delivery_number,
            'innings_runs': innings_runs,
            'innings_wickets': innings_wickets
        }])
        
        # Predict probability distribution
        probs = self.model.predict_proba(features)[0]
        
        # Ensure probs sum exactly to 1 for numpy choice
        probs = probs / np.sum(probs)
        
        # Sample an outcome index based on probabilities
        outcome_idx = np.random.choice(len(probs), p=probs)
        
        # Decode index to actual outcome
        outcome = self.le_y.inverse_transform([outcome_idx])[0]
        return outcome
