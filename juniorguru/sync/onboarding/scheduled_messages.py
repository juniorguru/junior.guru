SCHEDULED_MESSAGES = {}


def schedule_message(emoji):
    def decorator(render_text):
        SCHEDULED_MESSAGES[emoji] = render_text
    return decorator


@schedule_message('👋')
def render_hello(context):
    member = context['member']
    return f'Smrdíme v klubu, {member.display_name}!'


@schedule_message('🌯')
def render_burrito(context):
    member = context['member']
    return f'Žereme burrito, {member.display_name}'


@schedule_message('💤')
def render_sleep(context):
    member = context['member']
    return f'Spíme, {member.display_name}'


@schedule_message('🆗')
def render_ok(context):
    member = context['member']
    return f'Jsme OK, {member.display_name}'


@schedule_message('🟡')
def render_circle(context):
    member = context['member']
    return f'Hele žluté kolečko, {member.display_name}'


@schedule_message('🟥')
def render_square(context):
    member = context['member']
    return f'Hele červený čtvereček, {member.display_name}'


@schedule_message('🤡')
def render_clown(context):
    member = context['member']
    return f'Klauni toto!, {member.display_name}'
