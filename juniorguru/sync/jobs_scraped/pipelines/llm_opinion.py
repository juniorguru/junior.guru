import asyncio
import hashlib
import json
import os
from pprint import pprint

from diskcache import Cache
from openai import AsyncOpenAI
from openlimit import ChatRateLimiter

from juniorguru.lib import loggers


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are an assistant for classifying job postings in order to simplify job search
for entry level candidates who are looking for software engineering or software testing jobs.
Consider people who have just finished a coding bootcamp or a university degree in computer science.
User can provide a job posting and you reply with a valid JSON object, which contains the following keys:

- `is_entry_level` - boolean, whether the job posting is relevant to entry level candidates
- `reason` - string, short explanation why the job posting is entry level or not
- `is_sw_engineering` - boolean, whether the job posting is relevant to software engineering
- `is_sw_testing` - boolean, whether the job posting is relevant to software testing
- `tag_python` - boolean, whether the job posting wants Python
- `tag_javascript` - boolean, whether the job posting wants JavaScript
- `tag_java` - boolean, whether the job posting wants Java
- `tag_degree` - boolean, whether the job posting requires university degree
"""


logger = loggers.from_path(__file__)

rate_limiter = ChatRateLimiter(request_limit=500, token_limit=60000)


async def process(item: dict, cache: Cache | None = None) -> dict:
    user_prompt = f"{item['title']}\n\n{item['description_text']}"
    cache_key = f"llm_opinion_{hashlib.sha256(user_prompt.encode()).hexdigest()}"
    llm_opinion = cache.get(cache_key) if cache else None

    if llm_opinion:
        logger.debug(f"Using cached LLM opinion on {item['url']}")
    else:
        logger.debug(f"Asking for LLM opinion on {item['url']}")
        llm_opinion = await ask_llm(SYSTEM_PROMPT, user_prompt)
        if cache:
            cache.set(cache_key, llm_opinion)

    item["llm_opinion"] = llm_opinion
    return item


async def ask_llm(system_prompt: str, user_prompt: str) -> dict:
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    chat = dict(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        response_format=dict(type="json_object"),
    )
    async with rate_limiter.limit(**chat):
        completion = await client.chat.completions.create(**chat)

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
