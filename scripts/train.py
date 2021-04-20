import sqlite3
import pickle
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from juniorguru.lib.magic import UNIFIED_MODEL_PATH, UNIFIED_VECTORIZER_PATH, CS_VECTORIZER_PATH, CS_MODEL_PATH, \
    EN_VECTORIZER_PATH, EN_MODEL_PATH, ML_DATA_DIR

BACKUPS_DIR = Path(__file__).parent.parent / 'db_backups'


def read_data(path):
    df = pd.DataFrame({'junior': [], 'text': [], 'lang': []})
    for file in Path.iterdir(path):
        with sqlite3.connect(file) as cnx:
            df = df.append(pd.read_sql_query(
                'SELECT 1 as junior, json_extract(item, "$.link") as link, json_extract(item, "$.description_text") as text, json_extract(item, "$.lang") as lang FROM job WHERE junior_rank > 0',
                cnx), ignore_index=True)
            df = df.append(pd.read_sql_query(
                'SELECT 0 as junior, json_extract(item, "$.link") as link, json_extract(item, "$.description_text") as text, json_extract(item, "$.lang") as lang FROM jobdropped WHERE type = "NotEntryLevel"',
                cnx), ignore_index=True)

    return df


def train(df: pd.DataFrame):
    # Load data
    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(df['text'].values)

    # Classify data
    classifier = MultinomialNB()
    targets = df['junior'].values
    classifier.fit(counts, targets)

    return vectorizer, classifier


ML_DATA_DIR.mkdir(parents=True, exist_ok=True)

df = read_data(BACKUPS_DIR)
df = df.drop_duplicates(subset='link')

df_cs = df[df.lang == 'cs']
df_en = df[df.lang == 'en']

print(f'Training on {df_cs.count()} CS and {df_en.count()} EN items.')

# Unified
vectorizer, classifier = train(df)
UNIFIED_VECTORIZER_PATH.write_bytes(pickle.dumps(vectorizer))
UNIFIED_MODEL_PATH.write_bytes(pickle.dumps(classifier))

# CS
vectorizer, classifier = train(df_cs)
CS_VECTORIZER_PATH.write_bytes(pickle.dumps(vectorizer))
CS_MODEL_PATH.write_bytes(pickle.dumps(classifier))

# EN
vectorizer, classifier = train(df_en)
EN_VECTORIZER_PATH.write_bytes(pickle.dumps(vectorizer))
EN_MODEL_PATH.write_bytes(pickle.dumps(classifier))
