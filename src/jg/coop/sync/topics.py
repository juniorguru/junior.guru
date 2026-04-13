import re
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Self

import click
import yaml
from pydantic import Field, HttpUrl, computed_field, field_validator, model_validator

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.discord_club import parse_channel_link
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.topic import TopicDiscussion, TopicMention


logger = loggers.from_path(__file__)


YAML_PATH = Path("src/jg/coop/data/topics.yml")


KEYWORDS = {
    re.compile(r"\b" + key + r"\b", re.IGNORECASE): value
    for key, value in {
        r"pyladies|pylady": "pyladies",
        r"aj\s*ty\s*v\s*it": "ajtyvit",
        r"beeit": "beeit",
        r"codea?cademy": "codecademy",
        r"code\s*wars": "codewars",
        r"core\s*skill": "coreskill",
        r"lovely\s*data": "lovelydata",
        r"cs50": "cs50",
        r"42\s*prague": "42prague",
        r"enget\w+": "engeto",
        r"czechitas": "czechitas",
        r"(datov\w+|digit\w+) akademi\w+": "czechitas",
        r"it[.\s]?network": "itnetwork",
        r"react\s*girls": "reactgirls",
        r"rails\s*girls": "railsgirls",
        r"python\w*": "python",
        r"js": "javascript",
        r"javascript\w*": "javascript",
        r"aoc": "adventofcode",
        r"advent\s*of\s*code": "adventofcode",
        r"sdacademy": "sdacademy",
        r"sda": "sdacademy",
        r"software\s*development\s*a[ck]adem\w+": "sdacademy",
        r"udemy": "udemy",
        r"learn2code": "skillmea",
        r"l2c": "skillmea",
        r"skillmea": "skillmea",
        r"robweb": "robweb",
        r"yablko\w*": "robweb",
        r"programko\.net": "programkonet",
        r"voborn[íi]k": "programkonet",
        r"webrebel\w*": "webrebel",
        r"weby\s*kvalitn[ěe]": "webykvalitne",
        r"weba[řr]ce\s*pod\s*rukou": "webykvalitne",
        r"prima\s*kurzy": "primakurzy",
        r"kurzy\.vsb": "kurzyvsb",
        r"všb": "kurzyvsb",
        r"[šs]kola\s*k[óo]d[uúů]": "skolakodu",
        r"edx": "edx",
        r"school\s*of\s*code": "schoolofcode",
        r"seduo": "seduo",
        r"scrimb\w+": "scrimba",
        r"egg\s*head": "egghead",
        r"free\s*code\s*camp\w*": "freecodecamp",
        r"street\s*of\s*code\w*": "streetofcode",
        r"soc": "streetofcode",
        r"inventi": "inventi",
        r"it[.\s]?absolvent": "itabsolvent",
        r"nau[čc][.\s]?m[ěe][.\s]?it": "entership",
        r"entership": "entership",
        r"nau[čc][.\s]?se[.\s]?python": "naucsepython",
        r"it\s*v\s*kurze": "itvkurze",
        r"pluralsight": "pluralsight",
        r"praha\s*coding\s*school": "prahacodingschool",
        r"hackni\s*svou\s*budoucnost": "hacknisvoubudoucnost",
        r"(šetek|šetk)\w*": "hacknisvoubudoucnost",
        r"david\w*\s*(setek|setk)\w*": "hacknisvoubudoucnost",
        r"django\s*girls": "djangogirls",
        r"coding\s*boo?tcamp( pra(ha|gue))?": "codingbootcamppraha",
        r"data4you": "codingbootcamppraha",
        r"green\s*fox( academy| akademi[ei])?": "greenfox",
        r"gfa": "greenfox",
        r"unicorn\w*": "unicornhatchery",
        r"\w*hatchery": "unicornhatchery",
        r"courser\w*": "coursera",
        r"udacity": "udacity",
        r"data\s*camp\w*": "datacamp",
        r"(it\s*)?step(\.org)?": "step",
        r"coders\s*lab": "coderslab",
        r"kitner\w*": "radekkitner",
        r"tvrd[íi]kov\w+": "lucietvrdikova",
        r"umimpython": "umimpython",
        r"jet\s*brains\s*academy": "jetbrains",
        r"robot?\s*dreams?": "robotdreams",
        r"dok[aá][zž]e[sš]\s*programovat": "dokazesprogramovat",
        r"len[eé]rtov\w+": "dokazesprogramovat",
        r"andrew\s*sharp": "sharpprogrammer",
        r"sharp\s*programmer": "sharpprogrammer",
        r"ok\s*[šs]kolení": "okskoleni",
        r"ok\s*[s]yst[eé]m": "okskoleni",
        r"it[\- ]?academy(\.sk)?": "itacademy",
        r"vita\.sk": "vita",
        r"vita\s?academy": "vita",
        r"scripteo": "scripteo",
        r"(vláďa|vladimír|vlada|vladimir)\s+macek": "scripteo",
        r"cesta\s*do\s*it": "cestadoit",
        r"petr\s*fiala": "cestadoit",
        r"mark[ée]ta\s*willis": "marketawillis",
    }.items()
}


class TopicConfig(YAMLConfig):
    name: str | None = None
    icon: str | None = None
    channels: list[HttpUrl] = Field(min_length=1)
    pages: list[str] = []

    @computed_field
    def channel_ids(self) -> list[int]:
        return [parse_channel_link(str(channel_url)) for channel_url in self.channels]

    @field_validator("channels")
    @classmethod
    def validate_channels(cls, value: list[HttpUrl]) -> list[HttpUrl]:
        for url in value:
            parse_channel_link(str(url))
        return value

    @model_validator(mode="after")
    def validate_name_and_icon(self) -> Self:
        if self.name and not self.icon:
            raise ValueError("Topic with a name must also define an icon")
        return self


class TopicsConfig(YAMLConfig):
    definitions: list[TopicConfig]


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--history-months", default=6, type=click.IntRange(min=1))
@db.connection_context()
def main(today: date, history_months: int):
    prev_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    since_at = datetime.combine(
        today - timedelta(days=history_months * 30), datetime.min.time()
    )
    logger.info(
        f"Loading topics config from {YAML_PATH} (history={history_months} months, since={since_at:%Y-%m-%d})"
    )
    topics_config = TopicsConfig(**yaml.safe_load(YAML_PATH.read_text()))
    logger.info(f"Loaded {len(topics_config.definitions)} topic channel definitions")

    logger.info("Recreating topic tables")
    db.drop_tables([TopicMention, TopicDiscussion])
    db.create_tables([TopicMention, TopicDiscussion])

    topics = {keyword: Counter() for keyword in KEYWORDS.values()}
    topic_channels_monthly_letters_counts = [
        round(
            sum(
                ClubMessage.channel_size(channel_id, since_at=since_at)
                for channel_id in topic_config.channel_ids
            )
            / history_months
        )
        for topic_config in topics_config.definitions
    ]
    logger.info("Computed topic channel monthly letters counts")

    for i, topic_config in enumerate(topics_config.definitions):
        logger.info(
            f"Saving topic channel "
            f"{repr(topic_config.name) if topic_config.name else 'with no name'} "
            f"(channels={len(topic_config.channel_ids)}, "
            f"monthly_letters_count={topic_channels_monthly_letters_counts[i]})"
        )
        if not topic_config.name:
            logger.warning("Topic has no name! It won't be listed on the club page!")
        TopicDiscussion.create(
            name=topic_config.name,
            channel_ids=topic_config.channel_ids,
            icon=topic_config.icon,
            monthly_letters_count=topic_channels_monthly_letters_counts[i],
            page_src_uris=topic_config.pages,
        )

    logger.info("Computing keyword mention stats")
    messages = ClubMessage.listing()
    for message in messages:
        for keyword_re, keyword in KEYWORDS.items():
            if keyword_re.search(message.content):
                topics[keyword]["mentions_count"] += 1

        if message.created_at.date() >= prev_month:
            for keyword_re, keyword in KEYWORDS.items():
                if keyword_re.search(message.content):
                    topics[keyword]["mentions_last_month_count"] += 1
    for name, data in topics.items():
        logger.info(
            f"Saving topic {name!r} (mentions={data['mentions_count']}, mentions_last_month={data['mentions_last_month_count']})"
        )
        TopicMention.create(**{"name": name, **data})
