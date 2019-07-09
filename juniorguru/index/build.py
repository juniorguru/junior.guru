import json
from pathlib import Path

from jinja2 import Template


data = dict(name='Honza')


template_path = Path(__file__).parent / 'template.html'
template = Template(template_path.read_text())

html_path = Path(__file__).parent.parent.parent / 'build' / 'index.html'
html_path.write_text(template.render(**data))
