from pathlib import Path

from juniorguru.templating import render_template


template_path = Path(__file__).parent / 'template.html'
render_template('/practice/', template_path, {})
