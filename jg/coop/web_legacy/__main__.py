import warnings
from pathlib import Path

from flask_frozen import FrozenFlaskWarning

from jg.coop.web_legacy import app, get_freezer


def main(dest_path: str | Path):
    dest_path = Path(dest_path).absolute()
    app.config["SERVER_NAME"] = "junior.guru"
    app.config["FREEZER_DESTINATION"] = dest_path
    app.config["FREEZER_REMOVE_EXTRA_FILES"] = False
    app.config["FREEZER_BASE_URL"] = "https://junior.guru"
    app.static_folder = dest_path / "static"

    warnings.filterwarnings("error", category=FrozenFlaskWarning)

    freezer = get_freezer(app)
    freezer.freeze()
