import asyncio
from collections import defaultdict
from pathlib import Path
from time import perf_counter_ns

import click

from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import (ClubMemberID, emoji_name,
                                         get_or_create_dm_channel,
                                         get_pinned_message_url, get_reaction,
                                         parse_message_url)
from juniorguru.models.base import db
from juniorguru.models.page import Page
from juniorguru.models.sync import Sync
from juniorguru.sync.pages import main as sync_pages


NOTES_END = '\n\n#} -->'

EMOJI_PROCESSED = '✅'


logger = loggers.from_path(__file__)


@click.command()
@click.pass_context
def main(context):
    with db.connection_context():
        sync = Sync.start(perf_counter_ns())
    context.obj = dict(sync=sync, skip_dependencies=False)
    context.invoke(sync_pages)
    discord_sync.run(process_pins)


@db.connection_context()
async def process_pins(client):
    emoji_mapping = {page.meta['emoji']: Path(page.path)
                     for page in Page.handbook_listing()}
    notes_mapping = defaultdict(list)

    dm_channel = await get_or_create_dm_channel(client.get_user(ClubMemberID.HONZA))
    count = 0
    async for message in dm_channel.history(limit=None):
        count += 1
        if not message.reactions:
            logger.debug(f'Skipping {message.jump_url}')
            continue
        if get_reaction(message.reactions, EMOJI_PROCESSED):
            logger.debug(f'Already processed {message.jump_url}')
            continue
        logger.info(f'Processing {message.jump_url}')
        for reaction in message.reactions:
            emoji = emoji_name(reaction.emoji)
            try:
                path = emoji_mapping[emoji]
            except KeyError:
                raise KeyError(f"Unknown emoji {emoji} in reactions to {message.jump_url} (known: {list(emoji_mapping)!r})")
            notes_mapping[path].append(message)
    logger.info(f'Done processing {count} messages, collected notes for {len(notes_mapping)} pages')

    for path, messages in notes_mapping.items():
        logger.info(f'Adding {len(messages)} notes to {path}')
        notes = []
        for message in messages:
            pinned_message_details = parse_message_url(get_pinned_message_url(message))
            channel = client.club_guild.get_channel_or_thread(pinned_message_details['channel_id'])
            pinned_message = await channel.fetch_message(pinned_message_details['message_id'])
            note = f'--- {pinned_message.jump_url}\n{pinned_message.content}\n---\n'
            notes.append(note)
        notes_text = '\n\n' + '\n\n'.join(notes) + NOTES_END
        path.write_text(path.read_text().replace(NOTES_END, notes_text))
        await asyncio.gather(*[message.add_reaction(EMOJI_PROCESSED) for message in messages])
