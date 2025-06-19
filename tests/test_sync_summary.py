from jg.coop.sync.summary import (
    simplify_channel_mentions,
    simplify_custom_emojis,
    simplify_member_mentions,
)


def test_simplify_channel_mentions():
    channel_mapping = {
        788826407412170752: "poradna",
        1075052469303906335: "kurzy",
    }
    text = """
        - Nevíš co dál? Popiš svou situaci do <#788826407412170752>
        - Vybíráš kurz? Založ vlákno v <#1075052469303906335>
        - Hledáš konkrétní recenze? Zkus vyhledávání
    """
    expected = """
        - Nevíš co dál? Popiš svou situaci do #poradna
        - Vybíráš kurz? Založ vlákno v #kurzy
        - Hledáš konkrétní recenze? Zkus vyhledávání
    """

    assert simplify_channel_mentions(text, channel_mapping) == expected


def test_simplify_channel_mentions_thread_names():
    channel_mapping = {
        788826407412170752: "poradna",
        1075052469303906335: "Hľadám svoje stratené IT sebavedomie",
        9280524693034443: "záznamy-akcí",
    }
    text = """
        - Nevíš co dál? Popiš svou situaci do <#788826407412170752>
        - Vybíráš kurz? Založ vlákno v <#1075052469303906335>
        - Hledáš konkrétní recenze? Zkus <#9280524693034443>
    """
    expected = """
        - Nevíš co dál? Popiš svou situaci do #poradna
        - Vybíráš kurz? Založ vlákno v <#Hľadám svoje stratené IT sebavedomie>
        - Hledáš konkrétní recenze? Zkus #záznamy-akcí
    """

    assert simplify_channel_mentions(text, channel_mapping) == expected


def test_simplify_member_mentions():
    text = """
        Ahoj <@1301837433553293396>! Myslím si, že <@652142810291765248> je fakt borec.
        Ale možná i <@1301837433553293396> je fakt borec.
    """
    expected = """
        Ahoj @member1! Myslím si, že @member2 je fakt borec.
        Ale možná i @member1 je fakt borec.
    """

    assert simplify_member_mentions(text) == expected


def test_simplify_custom_emojis():
    text = """
        na tomhle webu pro <:pyconcz:1117549571757842603> (není to rozhodně krásný kód)  jsem zkoušel víc utility přístup protože to už boostrap měl taky
        základní šablona pro https://cz.pycon.org/2019/programme/schedule/
    """
    expected = """
        na tomhle webu pro :pyconcz: (není to rozhodně krásný kód)  jsem zkoušel víc utility přístup protože to už boostrap měl taky
        základní šablona pro https://cz.pycon.org/2019/programme/schedule/
    """

    assert simplify_custom_emojis(text) == expected


def test_simplify_custom_emojis_animated():
    text = """
        Myslím, že tam hraje hodně velkou rolik Microsoft? <a:batmanhmm:1080478927786610858>
    """
    expected = """
        Myslím, že tam hraje hodně velkou rolik Microsoft? :batmanhmm:
    """

    assert simplify_custom_emojis(text) == expected
