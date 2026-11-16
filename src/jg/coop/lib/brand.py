"""Names and links which identify junior.guru across the web, the API, and Discord."""

SITE_URL = "https://junior.guru/"

SITE_NAME = "junior.guru"

SITE_ALTERNATE_NAMES = ["Junior Guru"]

FOUNDER_NAME = "Honza Javorek"

YOUTUBE_URL = "https://www.youtube.com/@juniordotguru"

LINKEDIN_URL = "https://www.linkedin.com/company/juniorguru"

GITHUB_URL = "https://github.com/juniorguru/"

INSTAGRAM_URL = "https://www.instagram.com/juniordotguru"

TIKTOK_URL = "https://www.tiktok.com/@juniordotguru"

PODCAST_NAME = "Junior Guru: programování a kariéra v IT"

PODCAST_URL = f"{SITE_URL}podcast/"

PODCAST_FEED_URL = f"{SITE_URL}api/podcast.xml"

PODCAST_IMAGE_URL = f"{SITE_URL}static/podcast-v1.png"

PODCAST_SPOTIFY_URL = "https://open.spotify.com/show/12w93IKRzfCsgo7XrGEVw4"

PODCAST_APPLE_URL = (
    "https://podcasts.apple.com/cz/podcast/junior-guru-podcast/id1603653549"
)


def site_url(path: str = "") -> str:
    return f"{SITE_URL}{path.removeprefix('/')}"


def static_url(path: str) -> str:
    return site_url(f"static/{path.removeprefix('/')}")
