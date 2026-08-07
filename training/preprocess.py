from pathlib import Path

import pandas as pd

from backend.app.services.nlp import preprocess_text

RAW_DATA = Path('datasets/raw/resume_dataset.csv')
PROCESSED_DATA = Path('datasets/processed/resume_dataset_processed.csv')


def main():
    if not RAW_DATA.exists():
        raise FileNotFoundError(f'{RAW_DATA} not found')

    df = pd.read_csv(RAW_DATA)
    text_col = 'resume_text' if 'resume_text' in df.columns else df.columns[0]
    label_col = 'category' if 'category' in df.columns else df.columns[1]

    df = df[[text_col, label_col]].rename(columns={text_col: 'resume_text', label_col: 'category'})
    df['clean_text'] = df['resume_text'].fillna('').apply(preprocess_text)

    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA, index=False)
    print(f'Preprocessed data saved to {PROCESSED_DATA}')


if __name__ == '__main__':
    main()
