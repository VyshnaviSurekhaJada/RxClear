"""Disease prediction using trained Random Forest model."""
import os
import pickle
import numpy as np
from typing import Optional

_MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/disease_model.pkl')
_model_bundle: Optional[dict] = None


def _load_model() -> dict:
    global _model_bundle
    if _model_bundle is None:
        with open(_MODEL_PATH, 'rb') as f:
            _model_bundle = pickle.load(f)
    return _model_bundle


def predict_disease(medicine_names: list[str]) -> dict:
    """
    Predict probable disease(s) from a list of medicine names.
    Returns top-3 predictions with confidence scores.
    """
    if not medicine_names:
        return {'predictions': [], 'top_disease': None, 'confidence': 0}

    bundle = _load_model()
    model = bundle['model']
    vectorizer = bundle['vectorizer']
    le = bundle['label_encoder']

    # Normalize and sort for consistent feature representation
    query = ' '.join(sorted([m.lower().strip() for m in medicine_names]))

    X = vectorizer.transform([query])
    probs = model.predict_proba(X)[0]

    # Top 3 predictions
    top_indices = np.argsort(probs)[::-1][:3]
    predictions = []
    for idx in top_indices:
        if probs[idx] > 0.05:   # only include if ≥5% confidence
            predictions.append({
                'disease': le.classes_[idx],
                'confidence': round(float(probs[idx]) * 100, 1),
            })

    top = predictions[0] if predictions else None
    return {
        'predictions': predictions,
        'top_disease': top['disease'] if top else 'Undetermined',
        'confidence': top['confidence'] if top else 0,
    }
