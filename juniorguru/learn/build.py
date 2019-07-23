from pathlib import Path

import arrow

from juniorguru.templating import render_template


data = dict(year=arrow.utcnow().year)


template_path = Path(__file__).parent / 'template.html'
render_template('/learn/', template_path, data)
