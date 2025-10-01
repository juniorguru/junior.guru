import re
from collections import Counter
from datetime import date, timedelta

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.club import ClubMessage
from jg.coop.models.topic import Topic


logger = loggers.from_path(__file__)


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

TOPIC_CHANNELS = {
    re.compile(key): value
    for key, value in {
        r"^adventofcode$": "adventofcode",
    }.items()
}


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@db.connection_context()
def main(today: date):
    prev_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)

    Topic.drop_table()
    Topic.create_table()

    topics = {keyword: Counter() for keyword in KEYWORDS.values()}
    messages = ClubMessage.listing()
    for message in messages:
        topic_channel_keyword = get_topic_channel_keyword(message.channel_name)
        if topic_channel_keyword:
            topics.setdefault(topic_channel_keyword, Counter())
            topics[topic_channel_keyword]["topic_channels_messages_count"] += 1

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


def get_topic_channel_keyword(channel_name):
    for keyword_re, keyword in TOPIC_CHANNELS.items():
        if keyword_re.search(channel_name):
            return keyword
    return None
