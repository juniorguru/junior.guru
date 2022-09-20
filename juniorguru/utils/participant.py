import shutil
from pathlib import Path

from invoke import Exit, task
from slugify import slugify

from juniorguru.lib import loggers
from juniorguru.lib.images import downsize_square_photo, replace_with_jpg


AVATARS_DIR = Path(__file__).parent.parent / 'images' / 'avatars-participants'

AVATAR_SIZE_PX = 500


logger = loggers.get(__name__)


@task(name='participant')
def main(context, image_path):
    image_path = Path(image_path)

    if image_path.parent == AVATARS_DIR:
        logger.error(f'The image is already in {AVATARS_DIR}, oops')
        raise Exit(code=1)

    name = slugify(input('Participant name: '))
    destination_path = AVATARS_DIR / f'{name}{image_path.suffix}'

    logger.info(f'Copying the image to {destination_path}')
    image_path = Path(shutil.copy2(image_path, destination_path))

    logger.info('Processing the image')
    try:
        image_path = replace_with_jpg(downsize_square_photo(image_path, AVATAR_SIZE_PX))
    except Exception:
        image_path.unlink()
        raise

    logger.info(f'New image: {image_path}')
