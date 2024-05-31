from enum import StrEnum, auto

from pydantic import BaseModel

from jg.coop.lib import loggers
from jg.coop.lib.llm import ask_for_json
from jg.coop.lib.mutations import MutationsNotAllowedError
from jg.coop.sync.jobs_scraped import DropItem


SYSTEM_PROMPT = """
You are assistant for classifying job postings to simplify job search
for people who have just finished a coding bootcamp and who are looking
for SW engineering, SW testing, or data analyst jobs. User provides a job posting and you reply
with a valid JSON object containing the following keys:

- is_entry_level (bool) - Is it relevant to entry level candidates?
- reason_cs (string) - Short explanation why it is entry level or not, written in Czech
- field_engineering (bool) - Is it relevant to SW engineering?
- field_testing (bool) - Is it relevant to SW testing?
- field_data (bool) - Is it relevant to data science or data analysis?
- tag_py (bool) - Is Python required?
- tag_java (bool) - Is Java required?
- tag_js (bool) - Is JavaScript or TypeScript required?
- tag_php (bool) - Is PHP required?
- tag_win (bool) - Is extensive Windows or Azure knowledge required?
- tag_linux (bool) - Is extensive Linux knowledge required?
- tag_csharp (bool) - Is C# or .NET required?
- tag_ruby (bool) - Is Ruby or RoR required?
- tag_c_cpp (bool) - Is C/C++ required?
- tag_node (bool) - Is Node.js required?
- tag_html_css (bool) - Is HTML and CSS required?
- tag_db (bool) - Is knowledge of SQL or any databases in general required?
- tag_api (bool) - Is knowledge of APIs (REST, GraphQL) required?
"""


logger = loggers.from_path(__file__)


class Field(StrEnum):
    engineering = auto()
    testing = auto()
    data = auto()


class Technology(StrEnum):
    py = auto()
    java = auto()
    js = auto()
    php = auto()
    win = auto()
    linux = auto()
    csharp = auto()
    ruby = auto()
    c_cpp = auto()
    node = auto()
    html_css = auto()
    db = auto()
    api = auto()


class LLMOpinion(BaseModel):
    is_entry_level: bool
    reason_cs: str
    fields: set[Field]
    technologies: set[Technology]


async def process(item: dict) -> dict:
    try:
        llm_reply = await ask_for_json(
            SYSTEM_PROMPT,
            f"{item['title']}\n\n{item['description_text']}",
        )
    except MutationsNotAllowedError:
        raise DropItem("Asking LLM is not allowed")

    logger.debug(f"LLM reply (JSON): {llm_reply!r}")
    llm_opinion = LLMOpinion(
        is_entry_level=llm_reply["is_entry_level"],
        reason_cs=llm_reply["reason_cs"],
        fields={
            Field(key.removeprefix("field_"))
            for key, value in llm_reply.items()
            if key.startswith("field_") and value
        },
        technologies={
            Technology(key.removeprefix("tag_"))
            for key, value in llm_reply.items()
            if key.startswith("tag_") and value
        },
    )
    item["llm_opinion"] = llm_opinion.model_dump()
    logger.debug(f"LLM opinion: {item['llm_opinion']!r}")
    return item
