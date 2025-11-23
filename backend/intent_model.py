import joblib
import numpy as np
from embedding_extractor import get_embedding

# Load model once
clf, all_labels = joblib.load('intent_classifier.joblib')

def predict_intent(message):
    X = np.array([get_embedding(message)])
    y_pred = clf.predict(X)[0]
    predicted = [label for label, present in zip(all_labels, y_pred) if present]

    if not predicted:
        return ["no_intent_detected"]

    return predicted
