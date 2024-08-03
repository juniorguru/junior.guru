from pydantic import BaseModel

from jg.coop.lib import loggers
from jg.coop.lib.llm import ask_for_json
from jg.coop.lib.mutations import MutationsNotAllowedError
from jg.coop.sync.jobs_scraped import DropItem


SYSTEM_PROMPT = """
You're helping someone who has just learned programming to find their first job.
Decide if given job is relevant based on the following criteria:

- Involves at least some coding in a mainstream programming language
- Mentions it's for juniors, offers mentoring or onboarding, or otherwise seems beginner-friendly
- Requires at most 1 year, 1.5 years or 1+ years of experience
- DOES NOT involve responsibility for designing or architecting systems

User provides the job posting and you reply with a valid JSON object containing
the following keys:

- reason (string) - Concisely explain why you think the job is relevant or not, 200-300 characters
- is_relevant (bool) - Is the job relevant based on the above?
"""


logger = loggers.from_path(__file__)


class LLMOpinion(BaseModel):
    is_relevant: bool
    reason: str


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
        is_relevant=llm_reply["is_relevant"],
        reason=llm_reply["reason"],
    )
    item["llm_opinion"] = llm_opinion.model_dump()
    logger.debug(f"LLM opinion: {item['llm_opinion']!r}")
    return item
