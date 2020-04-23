from juniorguru.scrapers.middlewares import url_to_filename

import pytest


@pytest.mark.parametrize('url,expected', [
    ('https://stackoverflow.com/robots.txt',
     'robots.txt'),
    ('https://stackoverflow.com/jobs?sort=p&l=Se%C4%8D%2C+Czechia&u=Km',
     'jobs!sort=p&l=Seč, Czechia&u=Km.html'),
    ('https://stackoverflow.com/jobs/145568/software-engineer-m-f-java',
     'jobs!145568!software-engineer-m-f-java.html'),
])
def test_url_to_filename(url, expected):
    assert url_to_filename(url) == expected
