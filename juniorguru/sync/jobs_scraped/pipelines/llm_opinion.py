import json
import os

from openai import OpenAI


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


def process(item: dict) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"<h1>{item['title']}</h1>\n\n{item['description_html']}",
            },
        ],
        response_format=dict(type="json_object"),
    )
    choice = completion.choices[0]
    llm_opinion = json.loads(choice.message.content)
    llm_opinion["finish_reason"] = choice.finish_reason
    item["llm_opinion"] = llm_opinion
    return item


if __name__ == "__main__":
    item = process(
        {
            "title": "Webscraping analyst with Python",
            "description_html": """
                <div data-jobad="body" class="RichContent mb-1400"><p class="typography-body-medium-text-regular text-secondary mb-600">Pracovní nabídka</p><p class="typography-body-large-text-regular mb-800"><strong>Are you skilled in Python programming and passionate about data processing and analysis? </strong>Our Webscraping team is looking for a full-time Webscraping Analyst to join us in Prague or Ostrava. Our mission is to automate data collections and processing to simplify our colleagues' and clients' work. By scraping product information and company details across the web, we provide a complete market overview and make millions of data records accessible. </p><p class="typography-body-large-text-regular mb-800"><strong>What is the position about?</strong></p><ul class="typography-body-large-text-regular"><li>A to Z <strong>data processing</strong>, from scraping to processed data delivery. </li><li>Finding optimal solutions for <strong>various data sources. </strong></li><li>Learning new technologies for <strong>scraping and crawling data.</strong></li><li><strong>Automating </strong>data processing and classification. </li><li><strong>Helping research analysts</strong> understand their data needs and delivering solutions.</li></ul><p class="typography-body-large-text-regular mb-800"><strong>Technologies we use:</strong></p><ul class="typography-body-large-text-regular"><li>We use top technologies such as <strong>Mozenda </strong>and <strong>Playwright </strong>for scraping.</li><li><strong>Python </strong>(Pandas, NumPy, Seq2Seq, TF-IDF, etc.) for automation and data processing.</li><li><strong>Git </strong>to store and deploy our code.</li><li><strong>PostgreSQL </strong>and <strong>Snowflake </strong>as data storage. </li><li><strong>AWS </strong>infrastructure such as <strong>EC2, S3, SageMaker</strong>, among others.</li></ul><p class="typography-body-large-text-regular mb-800"><strong>What do we need from you?</strong></p><ul class="typography-body-large-text-regular"><li>To thrive in this role, you should ideally have <strong>advanced Python programming</strong> skills with experience using the Pandas library.</li><li><strong>Analytical </strong>thinking. </li><li>You must also be fluent in <strong>English (B2)</strong> to communicate with analysts from various regions, including North America, South America, Asia, and more.</li></ul><p class="typography-body-large-text-regular mb-800"><strong>Perks &amp; benefits:</strong></p><ul class="typography-body-large-text-regular"><li>We offer a unique opportunity to work on international projects, with daily communication in English and a guided introduction to everything you need to work independently.</li><li><strong>5 weeks</strong> of holidays<strong> + extra</strong> corporate <strong>days</strong> off</li><li><strong>Sick days</strong></li><li><strong>Flexibility</strong> to <strong>work from home</strong> most of the week</li><li>Certain <strong>flexibility</strong> to schedule your working hours</li><li><strong>Cafeteria system</strong> (you can use points on Flexipasses, pension or life insurance, or Multisport card. You can distribute points by your consideration)</li><li><strong>Meal allowance</strong> 90 CZK net/day</li></ul><p class="typography-body-large-text-regular mb-800"><br><strong>Join our team today and help us transform data into a valuable asset for our colleagues and clients!</strong></p></div>
             """,
        }
    )
    print(item["llm_opinion"])
