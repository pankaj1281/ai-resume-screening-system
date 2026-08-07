from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

try:
    from xgboost import XGBClassifier
except Exception:
    XGBClassifier = None

try:
    from lightgbm import LGBMClassifier
except Exception:
    LGBMClassifier = None

PROCESSED_DATA = Path('datasets/processed/resume_dataset_processed.csv')
MODEL_DIR = Path('models')


def build_models():
    return {
        'logistic_regression': LogisticRegression(max_iter=2000),
        'random_forest': RandomForestClassifier(n_estimators=300, random_state=42),
        'svm': SVC(probability=True, kernel='linear'),
        'naive_bayes': MultinomialNB(),
        'decision_tree': DecisionTreeClassifier(random_state=42),
        'knn': KNeighborsClassifier(n_neighbors=7),
        **({'xgboost': XGBClassifier(eval_metric='mlogloss')} if XGBClassifier else {}),
        **({'lightgbm': LGBMClassifier(verbose=-1)} if LGBMClassifier else {}),
    }


def main():
    if not PROCESSED_DATA.exists():
        raise FileNotFoundError(f'{PROCESSED_DATA} not found')

    df = pd.read_csv(PROCESSED_DATA)
    X = df['clean_text'].fillna('')
    y = df['category']

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    vectors = {
        'tfidf': TfidfVectorizer(max_features=15000, ngram_range=(1, 2)),
        'count': CountVectorizer(max_features=15000, ngram_range=(1, 2)),
    }

    best = {'acc': 0}
    for vector_name, vectorizer in vectors.items():
        for model_name, model in build_models().items():
            pipeline = Pipeline([('vectorizer', vectorizer), ('model', model)])
            scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')
            pipeline.fit(X_train, y_train)
            pred = pipeline.predict(X_test)
            acc = accuracy_score(y_test, pred)
            print(f'{vector_name}+{model_name} cv={scores.mean():.4f} test={acc:.4f}')
            if acc > best['acc']:
                best = {
                    'acc': acc,
                    'vectorizer': pipeline.named_steps['vectorizer'],
                    'model': pipeline.named_steps['model'],
                    'name': f'{vector_name}+{model_name}',
                }

    print('Best model baseline:', best['name'], best['acc'])

    # Mandatory GridSearchCV on logistic regression for tuned baseline
    gs = GridSearchCV(
        Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('model', LogisticRegression(max_iter=3000))
        ]),
        {
            'vectorizer__max_features': [10000, 15000],
            'vectorizer__ngram_range': [(1, 1), (1, 2)],
            'model__C': [0.5, 1.0, 2.0],
        },
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
    )
    gs.fit(X_train, y_train)
    tuned_pred = gs.best_estimator_.predict(X_test)
    tuned_acc = accuracy_score(y_test, tuned_pred)
    print('Tuned LogisticRegression:', gs.best_params_, tuned_acc)

    if tuned_acc >= best['acc']:
        model = gs.best_estimator_.named_steps['model']
        vectorizer = gs.best_estimator_.named_steps['vectorizer']
        selected = 'tfidf+tuned_logistic_regression'
        final_acc = tuned_acc
    else:
        model = best['model']
        vectorizer = best['vectorizer']
        selected = best['name']
        final_acc = best['acc']

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_DIR / 'model.joblib')
    joblib.dump(vectorizer, MODEL_DIR / 'vectorizer.joblib')
    joblib.dump(encoder, MODEL_DIR / 'label_encoder.joblib')

    print(f'Selected model: {selected} with accuracy={final_acc:.4f}')


if __name__ == '__main__':
    main()
