import tarfile
from pathlib import Path

DOWNLOAD_DIR = Path(__file__).parent.parent / 'backups'
TARGET_DIR = Path(__file__).parent.parent / 'db_backups'

def extract_backups(path: Path):
     TARGET_DIR.mkdir(exist_ok=True, parents=True)
     filepath: Path
     for filepath in path.iterdir():
         if tarfile.is_tarfile(filepath):
            print(f'Extracting {filepath}')
            tar = tarfile.open(filepath)
            filename = Path(filepath.stem).stem # .tar.gz, so we need two stems
            extracted = tar.extractfile('./juniorguru/data/data.db')
            target = Path(TARGET_DIR / f'{filename}.db')
            target.write_bytes(extracted.read())

extract_backups(DOWNLOAD_DIR)

