import argparse
from pathlib import Path

import joblib

from backend.app.services.nlp import preprocess_text

MODEL_DIR = Path('models')


def predict(text: str):
    model = joblib.load(MODEL_DIR / 'model.joblib')
    vectorizer = joblib.load(MODEL_DIR / 'vectorizer.joblib')
    encoder = joblib.load(MODEL_DIR / 'label_encoder.joblib')

    cleaned = preprocess_text(text)
    x = vectorizer.transform([cleaned])
    y = model.predict(x)
    label = encoder.inverse_transform(y)[0]
    return label


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', required=True)
    args = parser.parse_args()
    print(predict(args.text))
