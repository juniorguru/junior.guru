import random

from pydantic import BaseModel

from jg.coop.lib import loggers
from jg.coop.lib.llm import ask_llm
from jg.coop.lib.mutations import MutationsNotAllowedError, is_allowed
from jg.coop.sync.jobs_scraped import DropItem


logger = loggers.from_path(__file__)


class LLMOpinion(BaseModel):
    reason: str
    is_relevant: bool


async def process(item: dict) -> dict:
    try:
        llm_opinion = await ask_llm(
            """
                You're helping someone who has just learned programming to find their first job.
                Decide if given job is relevant based on the following criteria:

                - Involves at least some coding in a mainstream programming language
                - Mentions it's for juniors, offers mentoring or onboarding, or otherwise seems beginner-friendly
                - Requires maximum 2 years of experience
                - DOES NOT involve responsibility for designing or architecting systems (participating is ok, responsibility not ok)

                User provides the job posting and you reply with a valid JSON object containing
                the following keys:

                - reason (string) - Concisely explain why you think the job is relevant or not, 200-300 characters
                - is_relevant (bool) - Is the job relevant based on the above?
            """,
            f"{item['title']}\n\n{item['description_text']}",
            schema=LLMOpinion,
        )
    except MutationsNotAllowedError:
        if is_allowed("discord"):
            raise DropItem("Asking LLM is not allowed")
        else:
            logger.warning("Generating random opinion")
            llm_opinion = LLMOpinion(
                reason="Random opinion, because asking LLM was not allowed.",
                is_relevant=random.choice([True, False]),
            )

    logger.debug(f"LLM opinion: {llm_opinion!r}")
    item["llm_opinion"] = llm_opinion.model_dump()
    return item
