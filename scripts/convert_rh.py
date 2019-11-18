# To convert text from Red Hat job ads to Markdown. Usage:
#
# $ brew install pandoc
# $ pipenv run python scripts/convert_rh.py 'https://...' | pandoc -f html -t markdown_strict-raw_html | pbcopy

import sys

import requests
from lxml import html


response = requests.get(sys.argv[1])
response.raise_for_status()

html_tree = html.fromstring(response.content)
html_tree.make_links_absolute(response.url)

response = requests.get(html_tree.cssselect('iframe')[0].get('src'))
response.raise_for_status()

html_tree = html.fromstring(response.content)
html_tree.make_links_absolute(response.url)

job_content = html_tree.cssselect('.iCIMS_JobContent')[0]

for rubbish in job_content.cssselect('.iCIMS_JobContent > :not(.iCIMS_InfoMsg)'):
    rubbish.getparent().remove(rubbish)

print(html.tostring(job_content).decode('utf-8'))
