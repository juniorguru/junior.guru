import re
from pathlib import Path

import pytest

from juniorguru.sync.onboarding import scheduled_messages


scheduled_messages_source_code = Path(scheduled_messages.__file__).read_text()


@pytest.mark.parametrize('line, expected', [
    (line, f' # Day {n}')
    for n, line
    in enumerate((line for line in scheduled_messages_source_code.splitlines()
                  if line.startswith('@schedule_message')), start=1)
])
def test_scheduled_messages_comments(line, expected):
    assert line.endswith(expected)


@pytest.mark.parametrize('mention',
                         re.findall(r'<!?@!?\d+>', scheduled_messages_source_code))
def test_scheduled_messages_mentions(mention):
    assert '!' not in mention
    assert int(mention.lstrip('<@').rstrip('>')) in scheduled_messages.ALLOWED_MENTIONS
