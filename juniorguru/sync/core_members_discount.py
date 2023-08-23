import asyncio
from datetime import date, timedelta

from discord import ui

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers, mutations
from juniorguru.lib.discord_club import (
    ClubClient,
    ClubMemberID,
    get_or_create_dm_channel,
)
from juniorguru.lib.memberful import MemberfulAPI, memberful_url
from juniorguru.models.base import db
from juniorguru.models.club import ClubMessage, ClubUser


DISCOUNT_EMOJI = '🎂'

REMINDER_PERIOD_DAYS = 30 * 6

RECENT_PERIOD_DAYS = 30 * 6

RECENT_CONTENT_SIZE_THRESHOLD = 100

COUPON_SLUG = 'coremember'


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['members'])
def main():
    with db:
        members = ClubUser.core_discount_listing()
        logger.info(f"Members eligible: {len(members)}")
        logger.debug(f"Members eligible: {repr_members(members)}")

        members = [member for member in members
                   if member.recent_content_size(days=RECENT_PERIOD_DAYS) > RECENT_CONTENT_SIZE_THRESHOLD]
        logger.info(f"Members who recently wrote something: {len(members)}")
        logger.debug(f"Members who recently wrote something: {repr_members(members)}")

        members = [member for member in members
                   if is_recent_reminder(ClubMessage.last_bot_message(member.dm_channel_id, DISCOUNT_EMOJI))]
        logger.info(f"Members without offer: {len(members)}")
        logger.debug(f"Members without offer: {repr_members(members)}")

    if True:
        logger.info(f"Fetching details about the {COUPON_SLUG!r} discount")
        memberful = MemberfulAPI()
        coupons = memberful.get_nodes("""
            query fetch($cursor: String) {
                coupons(after: $cursor) {
                    totalCount
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                    edges {
                        node {
                            id
                            code
                            amountOffCents
                            isPercentage
                        }
                    }
                }
            }
        """)
        discount_info = get_discount_info(coupons, COUPON_SLUG)
    if members:
        logger.info("Sending offers")
        member_ids = [member.id for member in members]
        discord_sync.run(offer_core_discounts, discount_info, member_ids)


def is_recent_reminder(message: ClubMessage, today=None, days=REMINDER_PERIOD_DAYS) -> bool:
    today = today or date.today()
    reminder_period_starts_at = today - timedelta(days=days)
    if message:
        return message.created_at >= reminder_period_starts_at
    return False


def repr_members(members) -> str:
    return ', '.join(sorted([member.display_name for member in members], key=str.lower))


def get_discount_info(coupons, slug: str) -> dict:
    coupon = next(
        coupon for coupon in coupons
        if coupon['code'].lower().startswith(slug)
    )
    if coupon['isPercentage']:
        return dict(coupon=coupon['code'], ptc_off=coupon['amountOffCents'] // 100)
    raise NotImplementedError("Only percentage discounts are supported")


async def offer_core_discounts(client: ClubClient, discount_info: dict, members_ids: list[int]):
    await asyncio.gather(*[
        asyncio.create_task(offer_core_discount_to_member(client, discount_info, member_id))
        for member_id in members_ids
    ])


async def offer_core_discount_to_member(client: ClubClient, discount_info: dict, member_id: int):
    db_member = await asyncio.to_thread(get_member, member_id)
    logger.info(f"Offering core discount to {memberful_url(db_member.account_id)}")

    member = await client.club_guild.fetch_member(member_id)
    channel = await get_or_create_dm_channel(member)
    message_content = (
        f"{DISCOUNT_EMOJI} "
        f"Možná tomu ani nebudeš věřit, ale v klubu už jsi **{db_member.subscribed_days} dní**!"
        f"\n\n"
        f"Asi se ti tady fakt líbí 🥹 "
        f"Po takové době už nejsi žádný zelenáč. Víš, jak to tady chodí. Dokážeš leckomu poradit. "
        f"Patříš do jádra téhle komunity ❤️"
        f"\n\n"
        f"Chtěli bychom ti poděkovat za věrnost, ocenit tvé klubové zkušenosti "
        f"a motivovat tě, aby jsi s námi zůstal{'a' if db_member.has_feminine_name else ''} co nejdéle 🎁"
        f"\n\n"
        f"Předplatné ti bude **{db_member.expires_at:%-d.%-m.} končit** a Honza mě pověřil, "
        f"abych ti nabídlo slevu. Pokud chceš, klikni na tlačítko a použij kupón `{discount_info['coupon']}`. "
        f"**Sníží ti cenu všech budoucích objednávek o {discount_info['ptc_off']} %** <:shutupandtakemymoney:842465302783590441>"
        f"\n\n"
        f"Kdyby cokoliv nešlo, napiš <@{ClubMemberID.HONZA}>. "
        f"Kupón prosím nedávej nikomu jinému. Je pouze pro ty, kdo jsou v klubu dlouho."
    )
    button_url = f'https://juniorguru.memberful.com/account/subscriptions/{db_member.subscription_id}/coupons/new'
    buttons = [ui.Button(emoji='🏷️',
                         label='Zadat kupón',
                         url=button_url)]

    with mutations.mutating_discord(channel) as proxy:
        await proxy.send(message_content, view=ui.View(*buttons))


@db.connection_context()
def get_member(member_id: int) -> ClubUser:
    return ClubUser.get_by_id(member_id)
