from juniorguru.models.partner import Partner


BENEFITS_EVALUATORS = {}


def benefit(evaluate):
    slug = evaluate.__name__.replace('evaluate_', '')
    assert slug not in BENEFITS_EVALUATORS, 'Duplicate slug!'
    BENEFITS_EVALUATORS[slug] = evaluate


@benefit
def evaluate_logo_club(partnership):
    for partner in Partner.active_listing():
        if partner == partnership.partner:
            return True
    return False


@benefit
def evaluate_members(partnership):
    return len(partnership.partner.list_members) > 1


@benefit
def evaluate_welcome_club(partnership):
    intro = partnership.partner.intro
    if not intro:
        return False
    if intro.created_at.date() < partnership.starts_on:
        return False
    return True


@benefit
def evaluate_event_club(partnership):
    for event in partnership.partner.list_events:
        if event.start_at.date() > partnership.starts_on:
            return True
    return False


@benefit
def evaluate_job_1(partnership):
    return len(partnership.partner.list_jobs) > 0


@benefit
def evaluate_job_description(partnership):
    return len(partnership.partner.list_jobs) > 0


@benefit
def evaluate_job_2(partnership):
    return len(partnership.partner.list_jobs) > 1


@benefit
def evaluate_logo_handbook(partnership):
    for partner in Partner.handbook_listing():
        if partner == partnership.partner:
            return True
    return False


@benefit
def evaluate_podcast(partnership):
    for podcast_episode in partnership.partner.list_podcast_episodes:
        if podcast_episode.publish_on > partnership.starts_on:
            return True
    return False
