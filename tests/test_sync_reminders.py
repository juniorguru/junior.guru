from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.sync.reminders import ReminderConfig, build_reminder_content


def test_build_reminder_content():
    reminder = ReminderConfig(
        control_emoji="💡",
        channel_id=ClubChannelID.INTRO,
        content_template="Přečti si {👋}",
        period_days=30,
    )
    content = build_reminder_content(reminder, {"👋": "https://example.test"})

    assert content == "-# 💡 Přečti si https://example.test"


def test_build_reminder_content_resolves_role_mentions():
    reminder = ReminderConfig(
        control_emoji="🤝",
        channel_id=ClubChannelID.INTERVIEWS,
        content_template="Pro všechny <@&CANDIDATE>",
        period_days=7,
    )
    content = build_reminder_content(
        reminder, tip_urls_by_emoji={}, roles={"candidate": 1234567890}
    )

    assert content == "-# 🤝 Pro všechny <@&1234567890>"
