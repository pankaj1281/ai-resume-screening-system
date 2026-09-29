from pathlib import Path

import joblib

from ..config import settings
from .nlp import preprocess_text

REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_CATEGORIES = [
    "Data Scientist", "Machine Learning Engineer", "Software Engineer", "Frontend Developer",
    "Backend Developer", "Full Stack Developer", "Android Developer", "Cyber Security",
    "Cloud Engineer", "DevOps Engineer", "UI UX Designer", "Business Analyst",
    "Database Administrator", "Network Engineer"
]


class Predictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self._load()

    def _load(self):
        candidate_dirs = [Path(settings.model_dir), REPO_ROOT / "models", BACKEND_ROOT / "models"]
        seen = set()

        for model_dir in candidate_dirs:
            key = str(model_dir.resolve())
            if key in seen:
                continue
            seen.add(key)

            model_path = model_dir / "model.joblib"
            vec_path = model_dir / "vectorizer.joblib"
            enc_path = model_dir / "label_encoder.joblib"

            if model_path.exists() and vec_path.exists() and enc_path.exists():
                self.model = joblib.load(model_path)
                self.vectorizer = joblib.load(vec_path)
                self.label_encoder = joblib.load(enc_path)
                return

    def predict(self, text: str):
        if self.model is None:
            return {"category": "Software Engineer", "confidence": 0.51}

        cleaned = preprocess_text(text)
        x = self.vectorizer.transform([cleaned])
        pred = self.model.predict(x)[0]
        probs = self.model.predict_proba(x)[0] if hasattr(self.model, "predict_proba") else None
        if self.label_encoder is not None:
            category = self.label_encoder.inverse_transform([pred])[0]
        else:
            category = str(pred)
        confidence = float(max(probs)) if probs is not None else 0.75
        return {"category": category, "confidence": round(confidence, 4)}


predictor = Predictor()
