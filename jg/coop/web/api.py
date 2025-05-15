import csv
import gzip
import itertools
import json
from datetime import timedelta

import httpx
import ics
from pod2gen import Category, Episode, Funding, Media, Person, Podcast

from jg.coop.lib import apify
from jg.coop.lib.md import md
from jg.coop.models.base import db
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.event import Event
from jg.coop.models.job import ListedJob
from jg.coop.models.podcast import PodcastEpisode


@db.connection_context()
def build_course_providers_api(api_dir, config):
    course_providers = [
        {
            "cz_business_id": (
                str(cp.cz_business_id).zfill(8) if cp.cz_business_id else None
            ),
            "sk_business_id": (
                str(cp.sk_business_id).zfill(8) if cp.sk_business_id else None
            ),
        }
        for cp in CourseProvider.listing()
    ]
    api_file = api_dir / "course-providers.json"
    with api_file.open("w", encoding="utf-8") as f:
        json.dump(course_providers, f, ensure_ascii=False, indent=2)


@db.connection_context()
def build_events_ics(api_dir, config):
    calendar = ics.Calendar(
        events=[
            ics.Event(
                summary=event.title,
                begin=event.start_at,
                duration=timedelta(hours=1),
                description=event.url,
            )
            for event in Event.api_listing()
        ]
    )
    api_file = api_dir / "events.ics"
    with api_file.open("w", encoding="utf-8") as f:
        f.writelines(calendar)


@db.connection_context()
def build_events_honza_ics(api_dir, config):
    events = []
    for event in Event.api_listing():
        ics_event_promo_day = ics.Event(
            summary="(Honza by měl promovat klubovou akci)",
            begin=event.start_at - timedelta(days=7),
            description=event.url,
        )
        ics_event_promo_day.make_all_day()
        events.append(ics_event_promo_day)
        ics_event_day = ics.Event(
            summary="Akce v klubu",
            begin=event.start_at,
            description=event.url,
        )
        ics_event_day.make_all_day()
        events.append(ics_event_day)
        events.append(
            ics.Event(
                summary=f"{event.bio_name}: {event.title}",
                begin=event.start_at - timedelta(minutes=30),
                duration=timedelta(hours=3),
                description=event.url,
            )
        )
    calendar = ics.Calendar(events=events)
    api_file = api_dir / "events-honza.ics"
    with api_file.open("w", encoding="utf-8") as f:
        f.writelines(calendar)


@db.connection_context()
def build_czechitas_csv(api_dir, config):
    rows = [job.to_czechitas_api() for job in ListedJob.api_listing()]
    api_file = api_dir / "jobs.csv"
    with api_file.open("w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


@db.connection_context()
def build_navigara_api(api_dir, config):
    actor_names = [
        actor_name
        for actor_name in apify.fetch_scheduled_actors()
        if actor_name.startswith("honzajavorek/jobs-")
    ]
    items = itertools.chain.from_iterable(
        apify.fetch_data(actor_name, raise_if_missing=False)
        for actor_name in actor_names
    )

    api_subdir = api_dir / "navigara"
    api_subdir.mkdir(parents=True, exist_ok=True)

    api_file = api_subdir / "jobs.jsonl.gz"
    with gzip.GzipFile(api_file, mode="wb") as gzip_f:
        for item in items:
            line = json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n"
            gzip_f.write(line.encode("utf-8"))

    response = httpx.get(
        "https://raw.githubusercontent.com/"
        "juniorguru/plucker"  # repo
        "/refs/heads/main/"
        "jg/plucker/schemas/jobSchema.json",  # path
        follow_redirects=True,
    )
    response.raise_for_status()
    schema_file = api_subdir / "schema-apify.json"
    schema_file.write_bytes(response.content)


@db.connection_context()
def build_podcast_xml(api_dir, config):
    # TODO Category('Business'), Category('Education')
    # https://gitlab.com/caproni-podcast-publishing/pod2gen/-/issues/26

    person_hj = Person("Honza Javorek", "honza@junior.guru")
    podcast = Podcast(
        name="Junior Guru: programování a kariéra v IT",
        description="Jsme tu pro všechny juniory v IT! Jak začít s programováním? Jak najít práci v IT? Přinášíme odpovědi, inspiraci, motivaci.",
        language="cs",
        category=Category("Technology"),
        website="https://junior.guru/podcast/",
        feed_url="https://junior.guru/api/podcast.xml",
        authors=[Person("Pája Froňková"), person_hj],
        owner=person_hj,
        web_master=person_hj,
        copyright=f"© {PodcastEpisode.copyright_year()} Pavlína Froňková, Jan Javorek",
        generator="JuniorGuruBot (+https://junior.guru)",
        image="https://junior.guru/static/podcast-v1.png",
        fundings=[
            Funding("Přidej se do klubu junior.guru", "https://junior.guru/club/"),
            Funding("Přispěj junior.guru", "https://junior.guru/love/"),
        ],
        explicit=False,
    )

    club_ad = (
        "\n\n"
        "<hr>\n"
        "Jsou věci, se kterými ti kurz programování nepomůže. "
        "A proto je tady junior.guru. "
        "Průvodce na cestě do IT, který s tebou bude od začátku až do konce."
        "\n\n"
        "- **[Klub](https://junior.guru/club/):** "
        "Komunita na Discordu pro začátečníky a všechny, kdo jim chtějí pomáhat"
        "\n"
        "- **[Příručka](https://junior.guru/handbook/):** "
        "Rady, které ti pomůžou se základní orientací a se sháněním práce v oboru"
        "\n"
        "- **[Kurzy](https://junior.guru/courses/):** "
        "Katalog kurzů, ať si můžeš vybrat podle parametrů a recenzí, ne podle reklamy"
        "\n"
        "- **[Práce](https://junior.guru/jobs/):** "
        "Pracovní inzeráty vyloženě pro juniory, ať to nemusíš složitě hledat a třídit jinde"
        "\n"
        "- **[Inspirace](https://junior.guru/news/):** "
        "Podcasty, přednášky, články a další zdroje, které tě posunou a namotivují"
    )
    for number, db_episode in enumerate(PodcastEpisode.api_listing(), start=1):
        episode = Episode(
            id=db_episode.global_id,
            episode_number=number,
            episode_name=f"#{db_episode.number}",
            title=db_episode.format_title(number=True),
            image=f"https://junior.guru/static/{db_episode.image_path}",
            publication_date=db_episode.publish_at_prg,
            link=db_episode.url,
            summary=md(db_episode.description + club_ad),
            media=Media(
                db_episode.media_url,
                size=db_episode.media_size,
                type=db_episode.media_type,
                duration=timedelta(seconds=db_episode.media_duration_s),
            ),
        )
        podcast.add_episode(episode)

    podcast.rss_file(str(api_dir / "podcast.xml"))
