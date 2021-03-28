import tarfile
import os
from pathlib import Path

DOWNLOAD_DIR = Path(__file__).parent.parent / 'backups'
TARGET_DIR = Path(__file__).parent.parent / 'db_backups'

def extract_backups(path):
     os.makedirs(TARGET_DIR, exist_ok=True)
     for root, _, filenames in os.walk(path):
         tarfiles = filter(lambda file: tarfile.is_tarfile(os.path.join(root, file)), filenames)
         for filename in tarfiles:
            print(f'Extracting {filename}')
            filepath = os.path.join(root, filename)
            tar = tarfile.open(filepath)
            filename = filename.split('.')[0]
            extracted = tar.extractfile('./juniorguru/data/data.db')
            with open(os.path.join(TARGET_DIR,f'{filename}.db'), 'wb') as f:
                      f.write(extracted.read())


extract_backups(DOWNLOAD_DIR)

