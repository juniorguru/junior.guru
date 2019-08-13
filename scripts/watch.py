import time
from pathlib import Path
from subprocess import run

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


PROJECT_DIR = Path(__file__).parent.parent
PACKAGE_DIR = PROJECT_DIR / 'juniorguru'


def build():
    start = time.time()
    run(['pipenv', 'run', 'build'])
    seconds = int(time.time() - start)
    print(f'\nReady in {seconds}s')


class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f'Detected changes in {event.src_path}')
        build()


observer = Observer()
observer.schedule(EventHandler(), str(PACKAGE_DIR), recursive=True)
observer.start()

try:
    build()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('Stopping')
    observer.stop()

observer.join()
