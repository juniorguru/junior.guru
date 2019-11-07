import asyncio
from pathlib import Path

import aiofiles
import aiohttp


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0'


# async def fetch(session, url):
#     async with session.get(url) as response:
#         return response.status


# async def main(urls):
#     tasks = []
#     async with aiohttp.ClientSession() as session:
#         for url in urls:
#             tasks.append(fetch(session, url))
#         htmls = await asyncio.gather(*tasks)
#         for html in htmls:
#             print(html[:100])


async def main():
    seen_urls = set()
    files_queue = asyncio.Queue()
    urls_queue = asyncio.Queue()

    paths = Path(__file__).parent.parent.joinpath('build').glob('**/*.html')
    for path in paths:
        files_queue.put_nowait(path)

    files_workers = []
    for _ in range(3):
        files_workers.append(asyncio.create_task(
            file_worker(files_queue, seen_urls, urls_queue)
        ))

    await files_queue.join()
    for worker in files_workers:
        worker.cancel()
    await asyncio.gather(*files_workers, return_exceptions=True)

    urls_workers = []
    for _ in range(5):
        urls_workers.append(asyncio.create_task(
            url_worker(urls_queue)
        ))

    await urls_queue.join()
    for worker in urls_workers:
        worker.cancel()
    await asyncio.gather(*urls_workers, return_exceptions=True)


async def file_worker(files_queue, seen_urls, urls_queue):
    while True:
        path = await files_queue.get()
        print(path)
        for url in [
            'http://python.org',
            'https://google.com',
            'http://yifei.me'
        ]:
            if url not in seen_urls:
                urls_queue.put_nowait(url)
                seen_urls.add(url)
        files_queue.task_done()


async def url_worker(urls_queue):
    while True:
        url = await urls_queue.get()
        print(url)
        urls_queue.task_done()


if __name__ == '__main__':
    asyncio.run(main())
