import re
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

import click
import yaml
from pydantic import HttpUrl, computed_field, field_validator

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.discord_club import parse_channel_link
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.topic import Topic, TopicChannel


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
        r"nau[čc][.\s]?m[ěe][.\s]?it": "naucmeit",
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
    }.items()
}


class TopicConfig(YAMLConfig):
    name: str
    icon: str
    channels: list[HttpUrl]

    @computed_field
    def channel_ids(self) -> list[int]:
        return [parse_channel_link(str(channel_url)) for channel_url in self.channels]

    @field_validator("channels")
    @classmethod
    def validate_channels(cls, value: list[HttpUrl]) -> list[HttpUrl]:
        for url in value:
            parse_channel_link(str(url))
        return value


class TopicsConfig(YAMLConfig):
    definitions: list[TopicConfig]


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@db.connection_context()
def main(today: date):
    prev_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    since_at = datetime.combine(today - timedelta(days=182), datetime.min.time())
    topics_config = TopicsConfig(**yaml.safe_load(YAML_PATH.read_text()))

    Topic.drop_table()
    Topic.create_table()
    TopicChannel.drop_table()
    TopicChannel.create_table()

    topics = {keyword: Counter() for keyword in KEYWORDS.values()}
    topic_channels_content_sizes = {
        topic.name: 0 for topic in topics_config.definitions
    }

    for topic_config in topics_config.definitions:
        for channel_id in topic_config.channel_ids:
            parent_content_size = sum(
                message.content_size
                for message in ClubMessage.channel_listing(
                    channel_id,
                    parent=True,
                    since_at=since_at,
                )
            )
            channel_content_size = sum(
                message.content_size
                for message in ClubMessage.channel_listing(
                    channel_id,
                    parent=False,
                    since_at=since_at,
                )
            )
            topic_channels_content_sizes[topic_config.name] += (
                parent_content_size + channel_content_size
            )

    for topic_config in topics_config.definitions:
        TopicChannel.create(
            name=topic_config.name,
            icon=topic_config.icon,
            content_size=topic_channels_content_sizes[topic_config.name],
        )

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
        logger.info(f"{name} {dict(data)}")
        Topic.create(**{"name": name, **data})
