import pickle
from pandas import DataFrame
from pathlib import Path
from juniorguru.models import Employment


ML_DATA_DIR = Path(__file__).parent.parent.parent / 'juniorguru' / 'data' / 'ai'
UNIFIED_MODEL_PATH = ML_DATA_DIR / 'unified.cls'
UNIFIED_VECTORIZER_PATH = ML_DATA_DIR / 'unified.vct'
CS_MODEL_PATH = ML_DATA_DIR / 'cs.cls'
CS_VECTORIZER_PATH = ML_DATA_DIR / 'cs.vct'
EN_MODEL_PATH = ML_DATA_DIR / 'en.cls'
EN_VECTORIZER_PATH = ML_DATA_DIR / 'en.vct'


# TODO predict by languages
def set_ai_opinion():
    employments = Employment.select().where(Employment.juniority_ai_opinion.is_null())
    data_frame = DataFrame({'text': [], 'lang': [], 'link': []})
    data_frame = data_frame.append([{'text': employment.description_text,
                                     'lang': employment.lang,
                                     'link': employment.url} for employment in employments])

    vectorizer = pickle.loads(UNIFIED_VECTORIZER_PATH.read_bytes())
    classifier = pickle.loads(UNIFIED_MODEL_PATH.read_bytes())

    if data_frame.size > 0:
        predictions = classifier.predict(vectorizer.transform(data_frame['text']))
        for employment, prediction in zip(employments, predictions):
            employment.juniority_ai_opinion = prediction
            employment.save()
