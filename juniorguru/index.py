import json
from pathlib import Path

from jinja2 import Template


data = dict(name='Honza')


template_path = Path(__file__).parent / 'index.html'
template = Template(template_path.read_text())

# json_path = Path(__file__).parent / 'index.json'
# json_path.write_text(json.dumps(data, indent=2))

html_path = Path(__file__).parent.parent / 'build' / 'index.html'
html_path.write_text(template.render(**data))
