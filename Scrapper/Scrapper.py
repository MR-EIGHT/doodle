import json
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

    def start(self):
        self.scrape_queue.put(self.start_url)
        self.scrape()

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def scrape(self):
        with open("output.json", "a", encoding='utf-8') as outfile:
            outfile.write('{ \n "Documents": [' + '\n')

        while len(self.url_set) != self.limit:
            result = dict()
            current_url = self.scrape_queue.get(timeout=10)
            self.url_set.add(current_url)
            root_url = '{}://{}'.format(urlparse(current_url).scheme,
                                        urlparse(current_url).netloc)
            page = requests.get(current_url)
            soup = BeautifulSoup(page.content, "html.parser")
            result['url'] = current_url
            result['title'] = soup.title.string

            texts = soup.findAll(text=True)
            visible_texts = filter(self.tag_visible, texts)
            texts = u" ".join(t.strip() for t in visible_texts)
            result['body'] = texts

            json_object = json.dumps(result, indent=4, ensure_ascii=False)
            with open("output.json", "a", encoding='utf-8') as outfile:
                outfile.write(json_object + ',')

            anchor_tags = soup.find_all('a', href=True)

            for link in anchor_tags:
                url = link['href']
                if url.startswith('/'):
                    url = urljoin(root_url, url)
                if url not in self.url_set:
                    self.scrape_queue.put(url)

        with open("output.json", "r", encoding='utf-8') as outfile:
            st = outfile.read()
            st = st.rstrip(',')
        with open("output.json", "w", encoding='utf-8') as outfile:
            outfile.write(st + '\n ] \n }')


if __name__ == '__main__':
    s = Scrapper('http://urmia.ac.ir', 5)
    s.start()
