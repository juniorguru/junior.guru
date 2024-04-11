from coop.lib import loggers
from coop.lib.llm import ask_for_json
from coop.lib.mutations import MutationsNotAllowedError
from coop.sync.jobs_scraped import DropItem


SYSTEM_PROMPT = """
You are assistant for classifying job postings to simplify job search
for people who have just finished a coding bootcamp and who are looking
for SW engineering or SW testing jobs. User provides a job posting and you reply
with a valid JSON object containing the following keys:

- is_entry_level (bool) - Is it relevant to entry level candidates?
- reason (string) - Short explanation why it is entry level or not
- is_sw_engineering (bool) - Is it relevant to SW engineering?
- is_sw_testing (bool) - Is it relevant to SW testing?
- tag_python (bool) - Do they want Python?
- tag_javascript (bool) - Do they want JavaScript?
- tag_java (bool) - Do they want Java?
- tag_degree (bool) - Do they require university degree?
"""


logger = loggers.from_path(__file__)


async def process(item: dict) -> dict:
    try:
        item["llm_opinion"] = await ask_for_json(
            SYSTEM_PROMPT,
            f"{item['title']}\n\n{item['description_text']}",
        )
    except MutationsNotAllowedError:
        raise DropItem("Asking LLM is not allowed")
    return item
