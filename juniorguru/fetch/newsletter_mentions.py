import re
import os

import arrow

from juniorguru.fetch.lib.mailchimp import (MailChimpClient, get_collection,
                                            get_link)
from juniorguru.models import Job, JobNewsletterMention, db


MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')


def main():
    with db:
        JobNewsletterMention.drop_table()
        JobNewsletterMention.create_table()

        api = MailChimpClient(MAILCHIMP_API_KEY)
        campaigns = get_collection(api.get('/campaigns/'), 'campaigns')
        for campaign in campaigns:
            data = api.get(get_link(campaign, 'content'), count=1000)
            for url in find_urls(data['html']):
                try:
                    job = Job.get_by_url(url)
                except (ValueError, Job.DoesNotExist):
                    pass
                else:
                    JobNewsletterMention.create(job=job,
                                                sent_at=arrow.get(campaign['send_time']).date(),
                                                link=campaign['long_archive_url'])


def find_urls(html):
    return re.findall(r'https?://[^\s"\']+', html)


if __name__ == '__main__':
    main()
