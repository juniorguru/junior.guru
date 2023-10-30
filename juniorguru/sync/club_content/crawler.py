import asyncio
from datetime import datetime, timedelta, timezone
from typing import Generator

from discord import DMChannel, Member, Message, Reaction, User
from discord.abc import GuildChannel

from juniorguru.lib import loggers
from juniorguru.lib.discord_club import (
    DEFAULT_CHANNELS_HISTORY_SINCE,
    ClubChannelID,
    ClubClient,
    ClubEmoji,
    emoji_name,
    fetch_threads,
    get_channel_name,
    get_or_create_dm_channel,
    get_parent_channel,
    is_member,
    is_thread_after,
)
from juniorguru.sync.club_content.store import (
    store_dm_channel,
    store_member,
    store_message,
    store_pin,
)


logger = loggers.from_path(__file__)


WORKERS_COUNT = 6

CHANNELS_HISTORY_SINCE = {
    ClubChannelID.FUN: timedelta(days=30),
    ClubChannelID.FUN_TOPICS: timedelta(days=30),
    ClubChannelID.INTRO: None,  # all history since ever
    ClubChannelID.BUSINESS: None,  # all history since ever
}

CHANNELS_SKIP = [
    # skip channels
    ClubChannelID.MODERATION,
    ClubChannelID.BOT,
    ClubChannelID.JOBS,
    # skip práce-bot (archived)
    834443926655598592,
    # skip *-tipy (deprecated)
    1059686551447142400,
    1165504449574342696,
    1024941155537920020,
    1087734674224324648,
    1057874612827979908,
    1143036639560613908,
    1168041084543303720,
    1045915707562532976,
    1095435785672601704,
    1088501115076747354,
    1014605535552733335,
    1049177102504710194,
    1152820829462204436,
    1164592788810256484,
    1030498500405891222,
    1166229519380787282,
    1015586076456398918,
    1152096109997609030,
    1088677548541616249,
    1021866310050791465,
    1085053625124003942,
    1014605593341866024,
    1062774831864631296,
    1056623381384020098,
    1110512531061100544,
    1141774310629978242,
    1163752969548877855,
    1072492479452033097,
    1084328822771560468,
    1157532078599065630,
    1164185626611027978,
    1168403593553006673,
    1168041134124187698,
    1161156171839836210,
    1164417358287351838,
    1159069172383350824,
    1075631540580667472,
    1148472135996686346,
    1042292122008682536,
    1061498440145698856,
    1130352621144789014,
    1168403534568509450,
    1051800375071612950,
    1147275053839429663,
    1100416078221410324,
    1039392695883407430,
    1124364481112326255,
    1164156719321071626,
    1147275062655865022,
    1062704904071823370,
    1028961439228117023,
    1016567370216656946,
    1031908434041376828,
    1166831270895042641,
    1051800340346966016,
    1014605551583367188,
    1065628114157310052,
    1014605573012082789,
    1064860732275036271,
    1112595304068431912,
    1166685226303500309,
    1148472142489464852,
    1063310653131083806,
    1162242896481755177,
    1057512328570077215,
    1027528472379273237,
    1091030879993864332,
    1085608130358026353,
    1168403590289829888,
    1130388371303301163,
    1086140865086500945,
    1152096105513889893,
    1044284956253372466,
    1167483480532328519,
    1059686499328733314,
    1165504438274883657,
    1138687769598754887,
    1122379862250893412,
    1105219519288459425,
    1067296797191577690,
    1105219527412822026,
    1042102752551112704,
    1081340288376774717,
    1168489879454355486,
    1052076279442194482,
    1168403612981010524,
    1099635614862811156,
    1119480881850109983,
    1087382869271388242,
    1017040846304055356,
    1082258327859380296,
    1130352660051132437,
    1042654117820108860,
    1107884307260915743,
    1127720911831838772,
    1095435779934802011,
    1137963054726905856,
    1115494714737700925,
    1122379932094443594,
    1095704787036680203,
    1014943774629179442,
    1161156220443443331,
    1077645188450750556,
    1119118495548981360,
    1017462408350007366,
    1116626678286925835,
    1118800862890954832,
    1017655188582060073,
    1161368765540335708,
    1063310632264409159,
    1077081068152295525,
    1040117599347949578,
    1148834774945898536,
    1143398981213376593,
    1015200692123750410,
    1014943735546654781,
    1166685178731696230,
    1014605554104152146,
    1167075143684726855,
    1141728891086585947,
    1015215789651005520,
    1018018218520084600,
    1014605602149896322,
    1158256692258164766,
    1050264449098989599,
    1014605576191361066,
    1153907946246389771,
    1131842210745286747,
    1099635610660118612,
    1130768838020042783,
    1144287116440899714,
    1015215786727579779,
    1095435789443272744,
    1071282921056505876,
    1164592773727535154,
    1146660687356104796,
    1167316731962859611,
    1024319064195211304,
    1152820759266349056,
    1160068657204969472,
    1017040861571321898,
    1142124029994602636,
    1165504486496813137,
    1161518098243911721,
    1165504512551825510,
    1058236842274725948,
    1054010786437152768,
    1111145694317772810,
    1121775408245911652,
    1058236843956654244,
    1142059369438134282,
    1045190826344579173,
    1039392662467387482,
    1014605580230467764,
    1051800378116669510,
    1073636393428992082,
    1161156217696157788,
    1119118493518938152,
    1014605606390341662,
    1118800802937585704,
    1160854673314562068,
    1156082427370938408,
    1117668927699427338,
    1082258345634836560,
    1037485104672546927,
    1151604187445067836,
    1156444804754985011,
    1156082396920287303,
    1042102710461276260,
    1139599953719738378,
    1110420919500947476,
    1128666613990830081,
    1141310269923016825,
    1149559501226250312,
    1067296786449973278,
    1147022833470423130,
    1049980602838954006,
    1126870050041761893,
    1045553216416383026,
    1152096194659635270,
    1081340350855131136,
    1039755016480772106,
    1027528458923941898,
    1019180174178263060,
    1156082400791629884,
    1098824757597716561,
    1138687711184691311,
    1080705066480185424,
    1128666657884213288,
    1031787921881190400,
    1105533620027928706,
    1081792084807262269,
    1107159558843019274,
    1135653576543326311,
    1085415967854698557,
    1017040844601184287,
    1095563169386209341,
    1095435793272676525,
    1156082393959120996,
    1073540529284972604,
    1151733576887435337,
    1057149796143616040,
    1046842051267932170,
    1128178160530366484,
    1108293707691733002,
    1054975436481892413,
    1014605556658479134,
    1095925550763229395,
    1165866966876164107,
    1052801116359905310,
    1063137341507653743,
    1151195974958587904,
    1120930236129882152,
    1021278420371517510,
    1069470950015389756,
    1132526817929068604,
    1062472505341779969,
    1056623421737414798,
    1087296703507484702,
    1121655050993946644,
    1014943766395764816,
]


async def crawl(client: ClubClient) -> None:
    logger.info("Crawling members")
    members = []
    tasks = []
    async for member in client.club_guild.fetch_members(limit=None):
        members.append(member)
        tasks.append(asyncio.create_task(store_member(member)))
    await asyncio.gather(*tasks)

    logger.info("Crawling club channels")
    queue = asyncio.Queue()
    for channel in client.club_guild.channels:
        if channel.type != "category" and channel.permissions_for(client.club_guild.me).read_messages:
            if channel.id not in CHANNELS_SKIP:
                queue.put_nowait(channel)
            else:
                logger.debug(
                    f"Skipping channel #{channel.id} {get_channel_name(channel)!r}"
                )

    workers = [
        asyncio.create_task(channel_worker(worker_no, queue))
        for worker_no in range(WORKERS_COUNT)
    ]

    logger.info("Adding DM channels")
    tasks = []
    for member in members:
        tasks.append(asyncio.create_task(crawl_dm_channel(queue, member)))
    await asyncio.gather(*tasks)

    # trick to prevent hangs if workers raise, see https://stackoverflow.com/a/60710981/325365
    queue_completed = asyncio.create_task(queue.join())
    await asyncio.wait([queue_completed, *workers], return_when=asyncio.FIRST_COMPLETED)

    # if there's a worker which raised
    if not queue_completed.done():
        workers_done = [worker for worker in workers if worker.done()]
        logger.warning(
            f"Some workers ({len(workers_done)} of {WORKERS_COUNT}) finished before the queue is done!"
        )
        workers_done[0].result()  # raises

    # cancel workers which are still runnning
    for worker in workers:
        worker.cancel()

    # return_exceptions=True silently collects CancelledError() exceptions
    await asyncio.gather(*workers, return_exceptions=True)


async def crawl_dm_channel(queue: asyncio.Queue, member: Member) -> None:
    channel = await get_or_create_dm_channel(member)
    if channel:
        logger["channels"].debug(
            f"Adding DM channel #{channel.id} for member {channel.recipient.display_name!r}"
        )
        queue.put_nowait(channel)
        await store_dm_channel(channel)


async def channel_worker(worker_no, queue) -> None:
    logger_cw = logger[worker_no]["channels"]
    while True:
        channel = await queue.get()
        logger_c = get_channel_logger(logger_cw, channel)
        logger_c.info(f"Crawling {get_channel_name(channel)!r}")

        history_since = CHANNELS_HISTORY_SINCE.get(
            get_parent_channel(channel).id, DEFAULT_CHANNELS_HISTORY_SINCE
        )
        if history_since is None:
            history_after = None
            logger_c.debug("Crawling all channel history")
        else:
            history_after = get_history_after(history_since)
            logger_c.debug(
                f"Crawling history after {history_after:%Y-%m-%d} ({history_since.days} days ago)"
            )

        threads = [
            thread
            async for thread in fetch_threads(channel)
            if is_thread_after(thread, after=history_after) and not thread.is_private()
        ]
        if threads:
            logger_c.info(f"Adding {len(threads)} threads")
        for thread in threads:
            logger_c.debug(
                f"Adding thread '{thread.name}' #{thread.id} {thread.jump_url}"
            )
            queue.put_nowait(thread)

        tasks = []
        async for message in fetch_messages(channel, after=history_after):
            db_message = await store_message(message)
            async for reacting_member in fetch_members_reacting_by_pin(
                message.reactions
            ):
                tasks.append(
                    asyncio.create_task(store_pin(db_message, reacting_member))
                )
        await asyncio.gather(*tasks)

        logger_c.debug(f"Done crawling {get_channel_name(channel)!r}")
        queue.task_done()


def get_channel_logger(
    logger: loggers.Logger, channel: GuildChannel | DMChannel
) -> loggers.Logger:
    parent_channel_id = get_parent_channel(channel).id
    logger = logger[parent_channel_id]
    if parent_channel_id != channel.id:
        logger = logger[channel.id]
    return logger


async def fetch_messages(
    channel: GuildChannel | DMChannel, after=None
) -> Generator[Message, None, None]:
    try:
        channel_history = channel.history
    except AttributeError:
        return  # channel type doesn't support history (e.g. forum)
    async for message in channel_history(limit=None, after=after):
        yield message


async def fetch_members_reacting_by_pin(
    reactions: list[Reaction],
) -> Generator[User | Member, None, None]:
    for reaction in reactions:
        if emoji_name(reaction.emoji) == ClubEmoji.PIN:
            async for user in reaction.users():
                if is_member(user):
                    yield user
            break


def get_history_after(history_since, now=None):
    if now:
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
    else:
        now = datetime.now(timezone.utc)
    return now - history_since
