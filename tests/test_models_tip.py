from jg.coop.models.tip import Tip


def test_to_guide_data():
    tip = Tip(
        slug="hello",
        position=1,
        emoji="👋",
        title="👋 Hello",
        title_text="Hello",
        edit_url="https://github.com/juniorguru/junior.guru/edit/main/hello.md",
        discord_url="https://discord.com/channels/1/2/3",
        lead="Say hello.",
        content="Longer content which is not part of the guide.",
    )

    assert tip.to_guide_data() == {
        "title_text": "Hello",
        "discord_url": "https://discord.com/channels/1/2/3",
        "lead": "Say hello.",
        "emoji": "👋",
    }
