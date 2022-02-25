from pathlib import Path

from strictyaml import Map, Optional, Seq, Str, Url, load

from juniorguru.lib.tasks import sync_task
from juniorguru.models import Supporter, db


schema = Seq(
    Map({
        'name': Str(),
        Optional('url'): Url(),
    })
)


@sync_task()
@db.connection_context()
def main():
    path = Path(__file__).parent.parent / 'data' / 'supporters.yml'
    records = [dict(last_name=record.data['name'].split()[-1], **record.data)
               for record in load(path.read_text(), schema)]

    Supporter.drop_table()
    Supporter.create_table()

    for record in records:
        Supporter.create(**record)
