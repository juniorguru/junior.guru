SCHEDULED_MESSAGES = {}


def schedule_message(emoji):
    def decorator(render_text):
        SCHEDULED_MESSAGES[emoji] = render_text
    return decorator


@schedule_message('👋')
def render_hello():
    return 'Smrdíme v klubu!'


@schedule_message('🌯')
def render_burrito():
    return 'Žereme burrito'


@schedule_message('💤')
def render_sleep():
    return 'Spíme'


@schedule_message('🆗')
def render_ok():
    return 'Jsme OK'


@schedule_message('🟡')
def render_circle():
    return 'Hele žluté kolečko'


@schedule_message('🟥')
def render_square():
    return 'Hele červený čtvereček'


@schedule_message('🤡')
def render_clown():
    return 'Klauni toto!'
