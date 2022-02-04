import emoji


EMOJI_RE = emoji.get_emoji_regexp()


def process(job):
    job.title = EMOJI_RE.sub('', job.title).strip()
    return job
