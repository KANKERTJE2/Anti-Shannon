import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os
from starlette.requests import Request
import logging

logger = logging.getLogger("wukong.ml")

class AnomalyDetector:
    """
    The Brain: ML-based Anomaly Detection.
    Uses Isolation Forest to detect outliers in request metadata.
    """
    def __init__(self, model_path: str = "wukong_model.pkl"):
        self.model_path = model_path
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
        
        if os.path.exists(self.model_path):
            self.load()

    def _extract_features(self, request: Request, body_len: int) -> list:
        """
        Extracts numerical features from a request for the model.
        Features:
        1. Path length
        2. Number of headers
        3. Number of query params
        4. Body length
        """
        return [
            len(request.url.path),
            len(request.headers),
            len(request.query_params),
            body_len
        ]

    def train(self, data: list):
        """
        Train the model on a list of feature vectors (normal traffic).
        """
        if not data:
            return
            
        X = np.array(data)
        self.model.fit(X)
        self.is_trained = True
        self.save()
        logger.info(f"🧠 ML: Model trained on {len(data)} samples.")

    def predict(self, features: list) -> int:
        """
        Returns -1 for anomaly, 1 for normal.
        """
        if not self.is_trained:
            return 1 # Fail open if not trained
            
        X = np.array([features])
        return self.model.predict(X)[0]

    def save(self):
        joblib.dump(self.model, self.model_path)

    def load(self):
        try:
            self.model = joblib.load(self.model_path)
            self.is_trained = True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
