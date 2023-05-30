from pathlib import Path
import warnings

import flask_frozen

from juniorguru.web_legacy import app, generate_job_pages, generate_jobs_region_pages


def main(dest_path: str | Path):
    dest_path = Path(dest_path).absolute()
    app.config['SERVER_NAME'] = 'junior.guru'
    app.config['FREEZER_DESTINATION'] = dest_path
    app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
    app.config['FREEZER_BASE_URL'] = 'https://junior.guru'
    app.static_folder=dest_path / 'static'

    warnings.filterwarnings('error', category=flask_frozen.FrozenFlaskWarning)

    freezer = flask_frozen.Freezer(app)
    freezer.register_generator(generate_job_pages)
    freezer.register_generator(generate_jobs_region_pages)
    freezer.freeze()
