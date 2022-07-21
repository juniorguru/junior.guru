SCHEDULED_MESSAGES = {}


def schedule_message(emoji):
    def decorator(render_text):
        SCHEDULED_MESSAGES[emoji] = render_text
    return decorator


@schedule_message('👋')
def render_hello(context):
    return 'Smrdíme v klubu!'


@schedule_message('🌯')
def render_burrito(context):
    return 'Žereme burrito'


@schedule_message('💤')
def render_sleep(context):
    return 'Spíme'


@schedule_message('🆗')
def render_ok(context):
    return 'Jsme OK'


@schedule_message('🟡')
def render_circle(context):
    return 'Hele žluté kolečko'


@schedule_message('🟥')
def render_square(context):
    return 'Hele červený čtvereček'


@schedule_message('🤡')
def render_clown(context):
    return 'Klauni toto!'
