import pickle
import pandas as pd
from pathlib import Path
from juniorguru.models import Job, JobDropped

ML_DATA_DIR = Path(__file__).parent.parent.parent / 'juniorguru' / 'data' / 'ml'
UNIFIED_MODEL_PATH = ML_DATA_DIR / 'magic.cls'
UNIFIED_VECTORIZER_PATH = ML_DATA_DIR / 'magic.vct'
CS_MODEL_PATH = ML_DATA_DIR / 'magic_cs.cls'
CS_VECTORIZER_PATH = ML_DATA_DIR / 'magic_cs.vct'
EN_MODEL_PATH = ML_DATA_DIR / 'magic_en.cls'
EN_VECTORIZER_PATH = ML_DATA_DIR / 'magic_en.vct'


def read_data_job():
    jobs = Job.select(Job.id, Job.item).where(Job.junior_rank > 0)
    df = map_jobs_to_df(jobs)

    return jobs, df


def read_data_jobdropped():
    jobsdropped = JobDropped.select(JobDropped.id, JobDropped.item).where(JobDropped.type == 'NotEntryLevel')
    df = map_jobs_to_df(jobsdropped)

    return jobsdropped, df


def map_jobs_to_df(jobs):
    df = pd.DataFrame({'id': [], 'text': [], 'lang': [], 'link': []})
    df = df.append(list(map(lambda job: {'id': job.id, 'text': job.item['description_text'], 'lang': job.item['lang'],
                                         'link': job.item.get('link', '')}, jobs)))

    return df


def predict(df: pd.DataFrame, vectorizer, classifier):
    predictions = classifier.predict(vectorizer.transform(df['text']))

    return predictions


def update_jobs(jobs, predictions):
    # bulk_update() would be better, but results in infinite loop
    for job, prediction in zip(jobs, predictions):
        job.magic_is_junior = prediction
        job.save()


def do_magic():
    jobs, df_jobs = read_data_job()
    jobsdropped, df_jobsdropped = read_data_jobdropped()

    vectorizer = pickle.loads(UNIFIED_VECTORIZER_PATH.read_bytes())
    classifier = pickle.loads(UNIFIED_MODEL_PATH.read_bytes())

    if df_jobs.size > 0:
        predictions_jobs = predict(df_jobs, vectorizer, classifier)
        update_jobs(jobs, predictions_jobs)

    if df_jobsdropped.size > 0:
        predictions_jobsdropped = predict(df_jobsdropped, vectorizer, classifier)
        update_jobs(jobsdropped, predictions_jobsdropped)

    # TODO Predict by languages
    return
