REQUIREMENTS_MAPPING = {
    'mainstream programming language': 'základy programování',
    'databases': 'databáze',
    'data analysis': 'datová analýza',
    'servers and operations': 'správa serverů',
    'web backend': 'webový backend',
    'web frontend': 'webový frontend',
    'mobile apps development': 'mobilní aplikace',
    'mobile apps': 'mobilní aplikace',
}


def job_requirement_filter(requirement):
    try:
        return REQUIREMENTS_MAPPING[requirement]
    except KeyError:
        return requirement


TYPES_MAPPING = {
    'full-time': 'plný úvazek',
    'part-time': 'částečný úvazek',
    'paid-internship': 'placená stáž',
    'unpaid-internship': 'neplacená stáž',
    'volunteering': 'dobrovolnictví',
}


def job_type_filter(type_):
    try:
        return TYPES_MAPPING[type_]
    except KeyError:
        return type_
