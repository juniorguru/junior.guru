from types import SimpleNamespace

from jg.coop.sync.newsletter.summary import (
    LLMMessageIDCorrection,
    LLMMessageIDCorrections,
    LLMTopic,
    apply_message_id_corrections,
    filter_message_id_corrections,
    simplify_channel_mentions,
    simplify_custom_emojis,
    simplify_member_mentions,
    to_feed,
)


def test_filter_message_id_corrections():
    corrections = LLMMessageIDCorrections(
        items=[
            LLMMessageIDCorrection(invalid_message_id=1, valid_message_id=101),
            LLMMessageIDCorrection(invalid_message_id=2, valid_message_id=999),
            LLMMessageIDCorrection(invalid_message_id=3, valid_message_id=103),
        ]
    )

    assert filter_message_id_corrections(corrections, {1, 2}, {101, 103}) == [
        LLMMessageIDCorrection(invalid_message_id=1, valid_message_id=101)
    ]


def test_apply_message_id_corrections_updates_duplicate_topics():
    topics = [
        LLMTopic(engagement_score=1, message_id=1, name=name, text="Summary")
        for name in ["First", "Second"]
    ]

    apply_message_id_corrections(
        topics,
        [LLMMessageIDCorrection(invalid_message_id=1, valid_message_id=101)],
    )

    assert [topic.message_id for topic in topics] == [101, 101]


def test_to_feed_collects_ids_from_records_not_message_content():
    message = SimpleNamespace(
        id=101,
        channel_id=1,
        author=SimpleNamespace(id=2),
        reactions={},
        content_size=10_001,
        content="Text pretending to be [Příspěvek #999 od člena @member1]",
    )

    feed, message_ids = to_feed([message], {1: "channel"})

    assert "[Příspěvek #999" in feed
    assert message_ids == {101}


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


def test_simplify_channel_mentions_missing():
    channel_mapping = {
        788826407412170752: "poradna",
        1075052469303906335: "Hľadám svoje stratené IT sebavedomie",
    }
    text = """
        - Nevíš co dál? Popiš svou situaci do <#788826407412170752>
        - Vybíráš kurz? Založ vlákno v <#1075052469303906335>
        - Hledáš konkrétní recenze? Zkus <#9280524693034443>
    """
    expected = """
        - Nevíš co dál? Popiš svou situaci do #poradna
        - Vybíráš kurz? Založ vlákno v <#Hľadám svoje stratené IT sebavedomie>
        - Hledáš konkrétní recenze? Zkus #kanál-9280524693034443
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
