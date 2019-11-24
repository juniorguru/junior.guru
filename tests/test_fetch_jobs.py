from datetime import datetime

from juniorguru.fetch.fetch_jobs import select_jobs


def create_job(id, **kwargs):
    return {
        'id': id,
        'timestamp': kwargs.get('timestamp', datetime(2019, 7, 6, 20, 24, 3)),
        'is_approved': kwargs.get('is_approved', True),
    }


def test_select_jobs_returns_only_approved_jobs():
    jobs = select_jobs([
        create_job(1, is_approved=True),
        create_job(2, is_approved=False),
        create_job(3, is_approved=True),
    ])
    assert set(job['id'] for job in jobs) == {1, 3}


def test_select_jobs_sorts_by_timestamp_desc():
    jobs = select_jobs([
        create_job(1, timestamp=datetime(2010, 7, 6, 20, 24, 3)),
        create_job(2, timestamp=datetime(2019, 7, 6, 20, 24, 3)),
        create_job(3, timestamp=datetime(2014, 7, 6, 20, 24, 3)),
    ])
    assert [job['id'] for job in jobs] == [2, 3, 1]
