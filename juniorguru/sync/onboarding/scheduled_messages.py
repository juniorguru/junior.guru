from textwrap import dedent


SCHEDULED_MESSAGES = {}


def schedule_message(emoji):
    def decorator(render_text):
        SCHEDULED_MESSAGES[emoji] = render_text
    return decorator


@schedule_message('👋')
def render_hello(context):
    member = context['member']
    text = dedent(f'''
        Ahoj {member.mention}! Já jsem kuře, zdejší bot. Pomáhám se vším, co by nemusel <@!668226181769986078> stíhat sám. Tento privátní kanál jsem vytvořil jen pro tebe.

        **Jak funguje tento kanál?** 💬
        V klubu se toho děje hodně, tak ti sem budu posílat tipy, jak se orientovat. Ptej se tady na cokoliv ohledně fungování klubu, klidně reaguj na jednotlivé tipy, posílej zpětnou vazbu. Já odpovídat neumím, ale vidí sem i moderátoři a se vším ti rádi pomůžou.

        **Jak funguju já?** 🤖
        Jsem ranní ptáče – vstanu, udělám všechnu svou práci a zbytek dne se do klubu už nekoukám. Tipy ti tedy budou chodit zhruba jednou denně.

        **Neboj se chyb** 💁
        Různých rad a pravidel ti sem postupně dám dost, takže si je určitě všechny nezapamatuješ a rozhodně uděláš něco jinak. To vůbec nevadí! Moderátoři tě rádi opraví, nebo nasměrují. Neboj se jich a ber je spíš jako pomocníky, ne policajty.
    ''')
    if member.intro:
        text += dedent('''
            **Představení ostatním** 👋
            Koukám, že už máš svoje představení v kanálu <#788823881024405544>. To je super! Pod tvou zprávou je teď vlákno (_thread_), kam mohou ostatní reagovat a kde můžeš případně něco doplnit. Krátké uvítání tam máš i ode mně.
        ''')
    else:
        text += dedent('''
            **Představ se ostatním** 👋
            První, co se hodí v klubu udělat, je představit se v kanálu <#788823881024405544>. Ostatní členové klubu se tak doví, co už máš za sebou a co je tvým cílem. Zajímá nás všechno, díky čemu tě poznáme, ale piš jen to, co chceš, abychom o tobě věděli. Povinné není nic, ale těžko ti dobře poradíme s kariérou nebo kurzem, pokud nebudeme znát tvou situaci.

            Co tě přivedlo do klubu? Jaké máš vzdělání a čím se teď živíš? Máš za sebou nějaké IT školy nebo kurzy? Jaké věci už umíš? Jak dlouho se zajímáš o programování? Co tě láká: weby, hry, datová analýza, mobilní appky…? Máš nějaký svůj projekt? Plánuješ si hledat práci v oboru? Kolik na to máš času?
        ''')
    if not member.has_avatar:
        text += dedent('''
            Když si navíc dáš i profilový obrázek, dostaneš ode mě roli <@&836959652100702248>. Udělat to můžeš v sekci Profily nebo Uživatelský profil (_Profiles_ nebo _User Profile_) ve svém nastavení na Discordu. Nemusí to být přímo fotka, jde pouze o to, abychom tu neměli deset Honzů, které nerozeznáme od sebe.
        ''')
    return text.strip()
