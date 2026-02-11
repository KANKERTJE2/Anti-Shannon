# Wukong ML Training Guide

## Training the Anomaly Detector

The Wukong `AnomalyDetector` needs to be trained on "normal" traffic to learn what safe behavior looks like.

### 1. Collect Normal Traffic Data
Run your application with Wukong enabled but in "Training Mode" (or log feature vectors).
For the prototype, you can use the interactive training script.

### 2. Run Training Script

```python
from wukong.detectors.anomaly import AnomalyDetector

# Example normal features: [path_len, headers_count, query_params, body_len]
normal_traffic = [
    [1, 5, 0, 0],   # GET /
    [10, 6, 1, 0],  # GET /api/users?id=1
    [15, 8, 0, 100],# POST /api/login
    # ... add thousands of samples ...
]

detector = AnomalyDetector()
detector.train(normal_traffic)
print("Model trained and saved to wukong_model.pkl")
```

### 3. Deploy
Ensure `wukong_model.pkl` is present in your working directory when starting the Wukong middleware.
