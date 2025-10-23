import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


ACTOR_NAME = "curious_coder/linkedin-jobs-scraper"


def transform_item(item: dict) -> dict:
    apply_url = clean_url(
        clean_validated_url(clean_proxied_url(item["applyUrl"]))
    )
    return dict(
        title=item["title"],
        posted_on=item["postedAt"],
        url=get_job_url(get_job_id(item["link"])),
        apply_url=apply_url or None,
        company_name=item["companyName"],
        company_url=item.get("companyWebsite"),
        company_logo_urls=[item["companyLogo"]],
        locations_raw=item["location"],
        employment_types=[item["employmentType"]],
        description_html=item["descriptionHtml"],
        source="linkedin",
        source_urls=[item["inputUrl"]],
    )


def get_job_url(job_id: str) -> str:
    return f"https://www.linkedin.com/jobs/view/{job_id}"


def get_job_id(url: str) -> str:
    if match := re.search(r"-(\d+)$", urlparse(url).path):
        return match.group(1)
    raise ValueError(f"Could not parse LinkedIn job ID: {url}")


def clean_proxied_url(url: str) -> str:
    proxied_url = get_param(url, "url")
    if proxied_url:
        proxied_url = strip_utm_params(proxied_url)
        return replace_in_params(
            proxied_url, "linkedin", "juniorguru", case_insensitive=True
        )
    return url


def clean_validated_url(url: str) -> str:
    if url and "validate.perfdrive.com" in url:
        if ssc_url := get_param(url, "ssc"):
            return ssc_url
        raise ValueError(f"Could not parse SSC URL: {url}")
    return url


def clean_url(url: str) -> str:
    if url and "linkedin.com" in url:
        return strip_params(url, ["refId", "trk", "trackingId"])
    if url and "talentify.io" in url:
        return strip_params(url, ["tdd"])
    if url and "neuvoo.cz" in url:
        return strip_params(url, ["puid"])
    if url and "lever.co" in url:
        return re.sub(r"/apply$", "/", url)
    url = strip_utm_params(url)
    url = replace_in_params(url, "linkedin", "juniorguru", case_insensitive=True)
    return url


# TODO, this is ugly copy-paste from plucker


UTM_PARAM_NAMES = ["utm_source", "utm_medium", "utm_campaign"]


def strip_params(url: str, param_names: list[str]) -> str:
    parts = urlparse(url)
    params = {
        name: value
        for name, value in parse_qs(parts.query).items()
        if name not in param_names
    }
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))


def strip_utm_params(url: str) -> str:
    return strip_params(url, UTM_PARAM_NAMES)


def set_params(url: str, params: dict[str, str | None]) -> str:
    parts = urlparse(url)
    url_params = {name: value for name, value in parse_qs(parts.query).items()}
    for name, value in params.items():
        url_params[name] = ["" if value is None else str(value)]
    query = urlencode(url_params, doseq=True)
    return urlunparse(parts._replace(query=query))


def get_param(url: str, param_name: str) -> str | None:
    parts = urlparse(url)
    values = parse_qs(parts.query).get(param_name, [])
    return values[0] if values else None


def get_params(url: str) -> dict[str, str]:
    qs = urlparse(url).query
    return {name: values[0] for name, values in parse_qs(qs).items()}


def increment_param(url: str, param_name: str, inc: int = 1) -> str:
    parts = urlparse(url)
    params = parse_qs(parts.query)
    params.setdefault(param_name, ["0"])
    params[param_name] = [str(int(params[param_name][0]) + inc)]
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))


def replace_in_params(
    url: str, s: str, repl: str, case_insensitive: bool = False
) -> str:
    parts = urlparse(url)
    params = parse_qs(parts.query)

    if case_insensitive:
        replace = lambda value: re.sub(re.escape(s), repl, value, flags=re.I)  # noqa: E731
    else:
        replace = lambda value: value.replace(s, repl)  # noqa: E731

    params = {
        param_name: [replace(value) for value in values]
        for param_name, values in params.items()
    }
    query = urlencode(params, doseq=True)
    return urlunparse(parts._replace(query=query))
