import re
import string
from functools import lru_cache

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


@lru_cache(maxsize=1)
def _init_nlp_resources():
    for resource in ["stopwords", "wordnet", "omw-1.4", "punkt"]:
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)
    return set(stopwords.words("english")), WordNetLemmatizer()


def preprocess_text(text: str) -> str:
    stops, lemmatizer = _init_nlp_resources()
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [lemmatizer.lemmatize(tok) for tok in text.split() if tok not in stops]
    return " ".join(tokens)


def extract_keywords(text: str) -> set[str]:
    clean = preprocess_text(text)
    return {token for token in clean.split() if len(token) > 2}
