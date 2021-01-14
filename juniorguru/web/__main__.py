import os
import warnings
from pathlib import Path

import flask_frozen

from juniorguru.web import app


def main():
    app.config['SERVER_NAME'] = 'junior.guru'
    app.config['FREEZER_DESTINATION'] = Path(app.root_path) / '..' / '..' / 'public'
    app.config['FREEZER_BASE_URL'] = 'https://junior.guru'
    app.config['FREEZER_STATIC_IGNORE'] = ['src']
    app.config['FREEZER_DESTINATION_IGNORE'] = ['now.json']

    warnings.filterwarnings('error', category=flask_frozen.FrozenFlaskWarning)

    freezer = flask_frozen.Freezer(app)
    freezer.freeze()


if __name__ == '__main__':
    main()
