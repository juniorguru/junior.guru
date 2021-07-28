import sqlite3
import pickle
import sys

import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# see https://github.com/honzajavorek/junior.guru/blob/master/scripts/draw_winners.py#L6
sys.path.append(str(Path(__file__).parent.parent))
from juniorguru.lib.magic import UNIFIED_MODEL_PATH, UNIFIED_VECTORIZER_PATH, VECTORIZERS, MODELS, ML_DATA_DIR, \
    load_vectorizers, load_classifiers

BACKUPS_DIR = Path(__file__).parent.parent / 'db_backups'
DATABASE_PATH = Path(__file__).parent.parent / 'juniorguru' / 'data' / 'data.db'


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


def re_train(df: pd.DataFrame, vectorizer, classifier):
    # Load data
    counts = vectorizer.transform(df['text'].values)

    # Classify data
    targets = df['junior'].values
    classifier.partial_fit(counts, targets)

    return classifier


def train_from_scratch():
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
    VECTORIZERS['CS'].write_bytes(pickle.dumps(vectorizer))
    MODELS['CS'].write_bytes(pickle.dumps(classifier))

    # EN
    vectorizer, classifier = train(df_en)
    VECTORIZERS['EN'].write_bytes(pickle.dumps(vectorizer))
    MODELS['EN'].write_bytes(pickle.dumps(classifier))


def read_recent_data(path):
    df = pd.DataFrame({'junior': [], 'text': [], 'lang': []})
    with sqlite3.connect(path) as cnx:
        df = df.append(pd.read_sql_query(
            'SELECT "1" as junior, json_extract(item, "$.description_text") as text, json_extract(item, "$.lang") as lang, upvotes_count, downvotes_count FROM job WHERE magic_is_junior = 0 AND upvotes_count > downvotes_count',
            cnx), ignore_index=True)
        df = df.append(pd.read_sql_query(
            'SELECT "0" as junior, json_extract(item, "$.description_text") as text, json_extract(item, "$.lang") as lang, upvotes_count, downvotes_count  FROM jobdropped WHERE type = "NotEntryLevel" AND magic_is_junior = 1 AND downvotes_count > upvotes_count',
            cnx), ignore_index=True)
    return df


def train_gradually():
    # read models
    vectorizers = load_vectorizers()
    classifiers = load_classifiers()
    # read non-matching texts
    df = read_recent_data(DATABASE_PATH)
    df_cs = df[df.lang == 'cs']
    df_en = df[df.lang == 'en']

    # re-train and store models
    # Unified
    if df["junior"].count() > 0:
        print(f'Updating unified model with {df["junior"].count()} items.')
        classifier = re_train(df, vectorizers[0], classifiers[0])
        UNIFIED_MODEL_PATH.write_bytes(pickle.dumps(classifier))

    # CS
    if df_cs["junior"].count() > 0:
        print(f'Updating CS model with {df_cs["junior"].count()} items.')
        classifier = re_train(df_cs, vectorizers[1]['CS'], classifiers[1]['CS'])
        MODELS['CS'].write_bytes(pickle.dumps(classifier))

    # EN
    if df_en["junior"].count() > 0:
        print(f'Updating EN model with {df_en["junior"].count()} items.')
        classifier = re_train(df_en, vectorizers[1]['EN'], classifiers[1]['EN'])
        MODELS['EN'].write_bytes(pickle.dumps(classifier))


if len(sys.argv) > 1 and sys.argv[1] == '--from-scratch':
    train_from_scratch()
else:
    train_gradually()
