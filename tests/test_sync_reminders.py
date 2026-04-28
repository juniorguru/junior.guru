from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.sync.reminders import ReminderConfig, build_reminder_content


def test_build_reminder_content():
    reminder = ReminderConfig(
        control_emoji="💡",
        channel_id=ClubChannelID.INTRO,
        content_template="Precti si {👋}",
        period_days=30,
    )
    content = build_reminder_content(reminder, {"👋": "https://example.test"})

    assert content == "💡 Precti si https://example.test"
