import asyncio
import json
import logging
import os
from datetime import timedelta
from functools import lru_cache
from pprint import pprint

from openai import AsyncOpenAI, InternalServerError, RateLimitError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from juniorguru.lib import loggers
from juniorguru.lib.cache import cache


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

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

limit = asyncio.Semaphore(4)


async def process(
    item: dict,
) -> dict:
    item["llm_opinion"] = await fetch_llm_opinion(
        SYSTEM_PROMPT,
        f"{item['title']}\n\n{item['description_text']}",
    )
    return item


@lru_cache
def get_client() -> AsyncOpenAI:
    logger.debug("Creating OpenAI client")
    return AsyncOpenAI(api_key=OPENAI_API_KEY)


retry_defaults = dict(
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.DEBUG),
    stop=stop_after_attempt(5),
)


@retry(
    retry=(
        retry_if_exception_type(RateLimitError)
        & retry_if_exception(
            lambda exception: exception.type == "requests"
            and "requests per day" not in exception.message
        )
    ),
    wait=wait_random_exponential(min=1, max=60),
    **retry_defaults,
)
@retry(
    retry=(
        retry_if_exception_type(RateLimitError)
        & retry_if_exception(lambda exception: exception.type == "tokens")
    ),
    wait=wait_random_exponential(min=60, max=5 * 60),
    **retry_defaults,
)
@retry(
    retry=retry_if_exception_type(InternalServerError),
    wait=wait_random_exponential(min=60, max=5 * 60),
    **retry_defaults,
)
@cache(expire=timedelta(days=60), tag="llm-opinion")
async def fetch_llm_opinion(system_prompt: str, user_prompt: str) -> dict:
    client = get_client()
    async with limit:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=dict(type="json_object"),
        )
    choice = completion.choices[0]
    llm_opinion = json.loads(choice.message.content)
    llm_opinion["finish_reason"] = choice.finish_reason
    return llm_opinion


if __name__ == "__main__":

    async def test():
        item = await process(
            {
                "url": "https://example.com/job/1234",
                "title": "Webscraping analyst with Python",
                "description_html": """
                    <div data-jobad="body" class="RichContent mb-1400"><p class="typography-body-medium-text-regular text-secondary mb-600">Pracovní nabídka</p><p class="typography-body-large-text-regular mb-800"><strong>Are you skilled in Python programming and passionate about data processing and analysis? </strong>Our Webscraping team is looking for a full-time Webscraping Analyst to join us in Prague or Ostrava. Our mission is to automate data collections and processing to simplify our colleagues' and clients' work. By scraping product information and company details across the web, we provide a complete market overview and make millions of data records accessible. </p><p class="typography-body-large-text-regular mb-800"><strong>What is the position about?</strong></p><ul class="typography-body-large-text-regular"><li>A to Z <strong>data processing</strong>, from scraping to processed data delivery. </li><li>Finding optimal solutions for <strong>various data sources. </strong></li><li>Learning new technologies for <strong>scraping and crawling data.</strong></li><li><strong>Automating </strong>data processing and classification. </li><li><strong>Helping research analysts</strong> understand their data needs and delivering solutions.</li></ul><p class="typography-body-large-text-regular mb-800"><strong>Technologies we use:</strong></p><ul class="typography-body-large-text-regular"><li>We use top technologies such as <strong>Mozenda </strong>and <strong>Playwright </strong>for scraping.</li><li><strong>Python </strong>(Pandas, NumPy, Seq2Seq, TF-IDF, etc.) for automation and data processing.</li><li><strong>Git </strong>to store and deploy our code.</li><li><strong>PostgreSQL </strong>and <strong>Snowflake </strong>as data storage. </li><li><strong>AWS </strong>infrastructure such as <strong>EC2, S3, SageMaker</strong>, among others.</li></ul><p class="typography-body-large-text-regular mb-800"><strong>What do we need from you?</strong></p><ul class="typography-body-large-text-regular"><li>To thrive in this role, you should ideally have <strong>advanced Python programming</strong> skills with experience using the Pandas library.</li><li><strong>Analytical </strong>thinking. </li><li>You must also be fluent in <strong>English (B2)</strong> to communicate with analysts from various regions, including North America, South America, Asia, and more.</li></ul><p class="typography-body-large-text-regular mb-800"><strong>Perks &amp; benefits:</strong></p><ul class="typography-body-large-text-regular"><li>We offer a unique opportunity to work on international projects, with daily communication in English and a guided introduction to everything you need to work independently.</li><li><strong>5 weeks</strong> of holidays<strong> + extra</strong> corporate <strong>days</strong> off</li><li><strong>Sick days</strong></li><li><strong>Flexibility</strong> to <strong>work from home</strong> most of the week</li><li>Certain <strong>flexibility</strong> to schedule your working hours</li><li><strong>Cafeteria system</strong> (you can use points on Flexipasses, pension or life insurance, or Multisport card. You can distribute points by your consideration)</li><li><strong>Meal allowance</strong> 90 CZK net/day</li></ul><p class="typography-body-large-text-regular mb-800"><br><strong>Join our team today and help us transform data into a valuable asset for our colleagues and clients!</strong></p></div>
                """,
            }
        )
        pprint(item["llm_opinion"])

    asyncio.run(test())
