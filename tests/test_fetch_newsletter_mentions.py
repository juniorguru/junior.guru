from juniorguru.fetch.newsletter_mentions import find_urls


def test_find_urls():
    assert find_urls('''
        <a href="https://junior.guru/jobs/34fa3ec07892dd3ff64458e2ccbf12578e00860483427e9e7c4847bc/">Stáž</a>
        ...
        https://junior.guru/candidate-handbook/
        ...
        http://example.com
        https://junior.guru/jobs/215426887eaaad9105ecf647d0ff24cf94de7c9eb47cc6f2c55e6921/
    ''') == [
        'https://junior.guru/jobs/34fa3ec07892dd3ff64458e2ccbf12578e00860483427e9e7c4847bc/',
        'https://junior.guru/candidate-handbook/',
        'http://example.com',
        'https://junior.guru/jobs/215426887eaaad9105ecf647d0ff24cf94de7c9eb47cc6f2c55e6921/',
    ]
