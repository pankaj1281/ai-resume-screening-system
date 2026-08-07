"""Download Kaggle resume dataset placeholder script."""

from pathlib import Path


DATASET_DIR = Path('datasets/raw')


def main():
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    print('Place Kaggle dataset CSV in datasets/raw/resume_dataset.csv')


if __name__ == '__main__':
    main()
