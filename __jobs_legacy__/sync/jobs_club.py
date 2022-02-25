import re

from juniorguru.lib.timer import measure
from juniorguru.lib import loggers
from juniorguru.lib.club import run_discord_task, is_discord_mutable
from juniorguru.models import ClubMessage, Employment, Job, db


JOBS_CHANNEL = 834443926655598592
JOBS_VOTING_CHANNEL = 841680291675242546  # TODO

URL_RE = re.compile(r'https?://\S+', re.I)


logger = loggers.get(__name__)


@measure()
def main():
    run_discord_task('juniorguru.sync.jobs_club.discord_task')


@db.connection_context()
async def discord_task(client):
    seen_urls = set()
    discord_channel = await client.fetch_channel(JOBS_CHANNEL)

    logger.info('Saving votes from channel history')
    for message in ClubMessage.channel_listing(JOBS_CHANNEL):
        job_url = get_first_url(message.content)
        if not job_url:
            continue
        seen_urls.add(job_url)
        try:
            employment = Employment.get_by_url(job_url)
            logger.info(f'Found {job_url}, has score {employment.juniority_votes_score} ({employment.juniority_votes_count} votes)')
            votes_score = message.upvotes_count - message.downvotes_count
            votes_count = message.upvotes_count + message.downvotes_count
            if employment.juniority_votes_score != votes_score or employment.juniority_votes_count != votes_count:
                logger.info(f'Updating {job_url}, new score {votes_score} ({votes_count} votes)')
                employment.juniority_votes_score = votes_score
                employment.juniority_votes_count = votes_count
                employment.save()
        except Employment.DoesNotExist:
            logger.info(f'Not found {job_url}')

    logger.info('Posting new jobs to the channel')
    for job in Job.listing():
        if job.effective_link in seen_urls:
            continue

        if is_discord_mutable():
            logger.info(f'Posting {job.effective_link}')
            content = f'**{job.title}**\n{job.company_name} – {job.location}\n{job.effective_link}'
            discord_message = await discord_channel.send(content)
            await discord_message.add_reaction('👍')
            await discord_message.add_reaction('👎')


def get_first_url(message_content):
    match = URL_RE.search(message_content)
    if match:
        return match.group(0)
    return None


if __name__ == '__main__':
    main()
