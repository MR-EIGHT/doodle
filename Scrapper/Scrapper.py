import concurrent.futures
import json
import threading
from queue import Queue
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment


class Scrapper:

    def __init__(self, url, limit):
        self.start_url = url
        self.limit = limit
        self.url_set = set([])
        self.scrape_queue = Queue()
        self.lock = threading.Lock()

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    def start(self):
        self.scrape_queue.put(self.start_url)
        while len(self.url_set) != self.limit:
            current_url = self.scrape_queue.get(timeout=20)
            print(f'url: {current_url} in: {current_url not in self.url_set}')

            with self.lock:
                if current_url not in self.url_set:
                    self.url_set.add(current_url)
                    self.executor.submit(self.scrape, current_url)
                else:
                    continue

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def scrape(self, current_url):
        result = dict()

        root_url = '{}://{}'.format(urlparse(current_url).scheme,
                                    urlparse(current_url).netloc)

        page = requests.get(current_url)
        soup = BeautifulSoup(page.content, "html.parser")
        result['url'] = current_url
        result['title'] = soup.title.string
        result['title'] = result.get('title').strip()

        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        texts = u" ".join(t.strip() for t in visible_texts)
        result['content'] = texts.strip()

        a = requests.post(url='http://127.0.0.1:8000/searchmate/api/', data=result)
        print(f"{result}\n{a.text}\n\n")

        anchor_tags = soup.find_all('a', href=True)

        for link in anchor_tags:
            url = link['href']
            if url.startswith('/'):
                url = urljoin(root_url, url)
            with self.lock:
                if url not in self.url_set:
                    self.scrape_queue.put(url)


if __name__ == '__main__':
    s = Scrapper('http://urmia.ac.ir', 300)
    s.start()
