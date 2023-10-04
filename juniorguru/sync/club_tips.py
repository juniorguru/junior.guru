import re
from pathlib import Path

import click
from discord import AllowedMentions

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.discord_club import (
    ClubChannelID,
    ClubClient,
    ClubMemberID,
    get_starting_emoji,
)
from juniorguru.lib.mutations import mutating_discord
from juniorguru.models.base import db
from juniorguru.models.club import ClubDocumentedRole


REFERENCE_RE = re.compile(r'''
    <
        (?P<prefix>[#@&]+)
        (?P<value>[^>]+)
    >
''', re.VERBOSE)


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['roles'])
@click.option('--path', 'tips_path', default='juniorguru/data/tips', type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path))
def main(tips_path):
    with db.connection_context():
        roles = {documented_role.slug: documented_role.id
                 for documented_role
                 in ClubDocumentedRole.listing()}
    tips = list(load_tips(tips_path, roles=roles))
    logger.info(f'Loaded {len(tips)} tips')
    discord_sync.run(sync_tips, tips)


def load_tips(tips_path: Path, roles=None):
    for tip_path in tips_path.glob('*.md'):
        if tip_path.name == 'README.md':
            continue
        logger.info(f'Loading tip {tip_path}')
        yield parse_tip(tip_path.read_text(), roles=roles)


def parse_tip(markdown: str, roles=None) -> dict:
    markdown = markdown.strip()
    roles = {slug.upper(): id for slug, id in (roles or {}).items()}

    try:
        title_match = re.search(r'^# (.+)\n', markdown)
        title = title_match.group(1).strip()
        markdown = markdown[title_match.end():].strip()
    except Exception as e:
        raise ValueError('Could not parse title') from e

    emoji = get_starting_emoji(title)
    if not emoji:
        raise ValueError(f'Could not parse emoji: {title!r}')

    markdown = re.sub(r'\n+## ', '\n## ', markdown)

    resolvers = {
        '@&': lambda value: roles[value],
        '@': lambda value: ClubMemberID[value],
        '#': lambda value: ClubChannelID[value],
    }
    def resolve_reference(match: re.Match) -> str:
        prefix = match.group('prefix')
        value = match.group('value')
        try:
            return f'<{prefix}{resolvers[prefix](value)}>'
        except Exception as e:
            raise ValueError(f'Could not parse reference: {prefix}{value!r}') from e
    markdown = REFERENCE_RE.sub(resolve_reference, markdown)

    return dict(emoji=emoji,
                title=title,
                content=markdown)


@db.connection_context()
async def sync_tips(client: ClubClient, tips: list[dict]):
    channel = await client.fetch_channel(ClubChannelID.TIPS)
    threads = {get_starting_emoji(thread.name): thread for thread in channel.threads}
    allowed_mentions = AllowedMentions(everyone=True, users=[], roles=False, replied_user=True)

    for tip in tips:
        if tip['emoji'] in threads:
            thread = threads[tip['emoji']]
            logger.info(f'Updating tip: {tip["title"]}')
            if thread.name != tip['title']:
                with mutating_discord(thread) as proxy:
                    await proxy.edit(name=tip['title'])
            message = await thread.fetch_message(thread.id)
            if message.content != tip['content']:
                with mutating_discord(message) as proxy:
                    await proxy.edit(content=tip['content'],
                                     suppress=True,
                                     allowed_mentions=allowed_mentions)
        else:
            logger.info(f'Creating tip: {tip["title"]}')
            with mutating_discord(channel) as proxy:
                thread = await proxy.create_thread(name=tip['title'],
                                                   content=tip['content'],
                                                   allowed_mentions=allowed_mentions)
                await thread.get_partial_message(thread.id).edit(suppress=True)
