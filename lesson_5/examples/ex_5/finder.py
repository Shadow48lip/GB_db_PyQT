# ======================= Потоки и многозадачность ============================
# ----------------------------- GUI и потоки ----------------------------------

# ----------------------- Класс "поискового движка" ---------------------------
from pprint import pprint
from urllib.request import urlopen
from threading import Thread
from queue import Queue
import re


class Finder:
    """ Класс "поискового движка" """

    def __init__(self, text, res_queue=None):
        self.text = text
        self.res_queue = res_queue
        self.is_alive = False

    def search_in_url(self, url):
        """ Искать text по указанному URL """
        print("-->>", url)
        f = urlopen(url)
        data = f.read().decode('utf-8')
        pattern = "<p>.*?{}.*?</p>".format(self.text)
        res = re.findall(pattern, data)
        return res

    def _in_urls(self, urls):
        """ Поиск текста по списку urls """
        self.is_alive = True
        for url in urls:
            # На каждом шаге выполняется проверка - не был ли остановлен поиск
            if not self.is_alive:
                break
            data = self.search_in_url(url)
            # Если есть очередь для результатов, то результат передаётся в эту очередь
            if self.res_queue is not None:
                self.res_queue.put((url, data))

        self.is_alive = False
        if self.res_queue is not None:
            # В результирующую очередь помещается None-флаг для сигнализации окончания поиска
            self.res_queue.put(None)
            self.res_queue.join()

    def search_in_urls(self, urls):
        """ Запуск поиска в отдельном потоке """
        t = Thread(target=self._in_urls, args=(urls, ))
        t.daemon = True
        t.start()

    def stop_search(self):
        """ Остановка поиска """
        self.is_alive = False


if __name__ == '__main__':
    urls = ['http://www.python.org/', 'https://habrahabr.ru/search/?q=%5Bpython%5D', 'https://python-scripts.com/']
    res_queue = Queue()
    finder = Finder('python', res_queue=res_queue)
    finder.search_in_urls(urls)
    while True:
        data = res_queue.get()
        if data is None:
            break
        pprint(data)
