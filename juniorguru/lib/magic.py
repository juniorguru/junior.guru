import pickle
import pandas as pd
from pathlib import Path
from juniorguru.models import Job, JobDropped

ML_DATA_DIR = Path(__file__).parent.parent.parent / 'juniorguru' / 'data' / 'ml'
UNIFIED_MODEL_PATH = ML_DATA_DIR / 'magic.cls'
UNIFIED_VECTORIZER_PATH = ML_DATA_DIR / 'magic.vct'
SUPPORTED_LANGUAGES = ['CS', 'EN']
VECTORIZERS = {
    'EN': ML_DATA_DIR / 'magic_en.vct',
    'CS': ML_DATA_DIR / 'magic_cs.vct',
}
MODELS = {
    'EN': ML_DATA_DIR / 'magic_en.cls',
    'CS': ML_DATA_DIR / 'magic_cs.cls',
}


def read_data_job():
    jobs = Job.select(Job.id, Job.item).where(Job.junior_rank > 0)
    df = map_jobs_to_df(jobs)

    return jobs, df


def read_data_jobdropped():
    jobsdropped = JobDropped.select(JobDropped.id, JobDropped.item).where(JobDropped.type == 'NotEntryLevel').execute()
    df = map_jobs_to_df(jobsdropped)

    return jobsdropped, df


def map_jobs_to_df(jobs):
    df = pd.DataFrame({'text': [], 'lang': [], 'link': []})
    df = df.append([{'text': job.item['description_text'], 'lang': job.item['lang'],
                     'link': job.item.get('link', '')} for job in jobs])

    return df


def predict(df: pd.DataFrame, vectorizers, classifiers):
    predictions = classifiers[0].predict(vectorizers[0].transform(df['text']))
    lang = df.lang[0].upper()
    language_predictions = None
    if lang in SUPPORTED_LANGUAGES:
        language_predictions = classifiers[1][lang].predict(vectorizers[1][lang].transform(df['text']))

    return predictions, language_predictions


def update_jobs(jobs, predictions):
    # bulk_update() would be better, but results in infinite loop
    for job, prediction, prediction_lang in zip(jobs, predictions[0], predictions[1]):
        job.magic_is_junior = prediction
        job.magic_is_junior_lang = prediction_lang
        job.save()


def do_magic():
    jobs, df_jobs = read_data_job()
    jobsdropped, df_jobsdropped = read_data_jobdropped()

    vectorizers = load_vectorizers()
    classifiers = load_classifiers()

    if df_jobs.size > 0:
        predictions_jobs = predict(df_jobs, vectorizers, classifiers)
        update_jobs(jobs, predictions_jobs)

    if df_jobsdropped.size > 0:
        predictions_jobsdropped = predict(df_jobsdropped, vectorizers, classifiers)
        update_jobs(jobsdropped, predictions_jobsdropped)


def load_classifiers():
    classifier = pickle.loads(UNIFIED_MODEL_PATH.read_bytes())
    language_classifiers = {}
    for language in SUPPORTED_LANGUAGES:
        language_classifiers[language] = pickle.loads(MODELS[language].read_bytes())

    return classifier, language_classifiers


def load_vectorizers():
    vectorizer = pickle.loads(UNIFIED_VECTORIZER_PATH.read_bytes())
    language_vectorizers = {}
    for language in SUPPORTED_LANGUAGES:
        language_vectorizers[language] = pickle.loads(VECTORIZERS[language].read_bytes())

    return vectorizer, language_vectorizers
