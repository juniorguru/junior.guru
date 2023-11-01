import re
from pprint import pformat

from juniorguru.lib import loggers
from juniorguru.lib.text import extract_text, split_blocks


# TODO add support for more abbreviations
SENTENCE_END_RE = re.compile(
    r"""
        (?<!\b(                 # must not be preceeded by the following abbreviations
            min
        ))
        (
            [\?\.\!\:\;…]+\ |   # common "end of sentence" chars followed by a space
            \.\.\.\ |           # literal form of … followed by a space
            \n                  # new line
        )
    """,
    re.VERBOSE,
)


logger = loggers.from_path(__file__)


def process(item):
    try:
        description_text = extract_text(item["description_html"])
        item["description_text"] = description_text
        item["description_sentences"] = split_sentences(description_text)
        # TODO item['description_words'] = split_words(description_text, job['lang'])
        return item
    except Exception:
        logger.exception(f"Unable to extract text from item:\n{pformat(item)}")
        raise


def split_sentences(text):
    """
    Splits given text into "sentences"

    The sentences are just approximate, there is no guarantee on correctness
    and there is no rocket science. The input text is assumed to have
    the guarantees provided by the extract_text() function.
    """
    return split_blocks(SENTENCE_END_RE.sub(r"\1\n\n", text))
