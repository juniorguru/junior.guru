import asyncio
import tarfile
from aiopath import AsyncPath as Path


DOWNLOAD_DIR = Path(__file__).parent.parent / 'backups'
TARGET_DIR = Path(__file__).parent.parent / 'db_backups'


async def extract(filepath: Path):
    if tarfile.is_tarfile(filepath):
        print(f'Extracting {filepath}')
        # tar stuff is blocking, but running it async overhead
        # resulted in longer total time
        tar = tarfile.open(filepath)
        filename = Path(filepath.stem).stem # .tar.gz, so we need two stems
        extracted = tar.extractfile('./juniorguru/data/data.db')
        target = Path(TARGET_DIR / f'{filename}.db')
        await target.write_bytes(extracted.read())


async def extract_backups(path: Path):
     await TARGET_DIR.mkdir(exist_ok=True, parents=True)
     await asyncio.wait([extract(p) async for p in path.iterdir()])


def main():
    asyncio.run(extract_backups(DOWNLOAD_DIR))


if __name__ == "__main__":
   main()
