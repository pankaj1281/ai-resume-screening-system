from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, precision_recall_fscore_support, roc_auc_score
from sklearn.model_selection import train_test_split

PROCESSED_DATA = Path('datasets/processed/resume_dataset_processed.csv')
MODEL_DIR = Path('models')
REPORT_DIR = Path('reports')


def main():
    df = pd.read_csv(PROCESSED_DATA)
    X_train, X_test, y_train, y_test = train_test_split(df['clean_text'].fillna(''), df['category'], test_size=0.2, random_state=42)

    model = joblib.load(MODEL_DIR / 'model.joblib')
    vectorizer = joblib.load(MODEL_DIR / 'vectorizer.joblib')
    encoder = joblib.load(MODEL_DIR / 'label_encoder.joblib')

    y_test_encoded = encoder.transform(y_test)
    X_test_vec = vectorizer.transform(X_test)
    pred = model.predict(X_test_vec)

    precision, recall, f1, _ = precision_recall_fscore_support(y_test_encoded, pred, average='weighted')
    print('Classification Report:')
    print(classification_report(y_test_encoded, pred, target_names=encoder.classes_))
    print({'precision': precision, 'recall': recall, 'f1': f1})

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ConfusionMatrixDisplay.from_predictions(y_test_encoded, pred)
    plt.title('Confusion Matrix')
    plt.savefig(REPORT_DIR / 'confusion_matrix.png', bbox_inches='tight')

    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(X_test_vec)
        roc = roc_auc_score(y_test_encoded, probs, multi_class='ovr')
        print({'roc_auc_ovr': roc})


if __name__ == '__main__':
    main()
