from pathlib import Path
import shutil


MODEL_DIR = Path('models')
BACKEND_MODEL_DIR = Path('backend/models')


def main():
    BACKEND_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    for name in ['model.joblib', 'vectorizer.joblib', 'label_encoder.joblib']:
        src = MODEL_DIR / name
        if src.exists():
            shutil.copy(src, BACKEND_MODEL_DIR / name)
            print(f'Copied {src} -> {BACKEND_MODEL_DIR / name}')


if __name__ == '__main__':
    main()
