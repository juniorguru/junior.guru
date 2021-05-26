from juniorguru.lib.log import get_log
from juniorguru.lib.club import discord_task
from juniorguru.models import ClubMessage, db


log = get_log('pins')


@discord_task
async def main(client):  # TODO
    with db:
        messages = ClubMessage.pins_listing()
    for message in messages:
        pass


if __name__ == '__main__':
    main()
