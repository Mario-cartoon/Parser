from urllib.parse import urljoin
from importlib import reload
from bs4 import BeautifulSoup
import requests as req
import json


class ParserStat:

    def __init__(self):
        self.url = 'https://habr.com/ru/users/newtechaudit/posts/page'

    def get_page_data(self):
        counter = 1
        data = {'info': []}
        try:
            while True:

                res = req.get("".join([self.url, str(counter)]))
                print("".join([self.url, str(counter)]))
                soup = BeautifulSoup(res.text, 'html.parser')
                page = soup.find('a', class_='tm-pagination__navigation-link tm-pagination__navigation-link_active')

                if page is None:
                    break
                items = soup.find_all('article', class_='tm-articles-list__item')
                for item in items:

                    try:
                        data['info'].append({
                            'titles': self.check_info('a', 'tm-article-snippet__title-link', item),
                            'times': self.check_info('span', 'tm-article-snippet__datetime-published', item),
                            'views': self.check_info('span', 'tm-icon-counter__value', item),
                            'saved': self.check_info('span', 'bookmarks-button__counter', item),
                            'karma': self.check_info('span', 'tm-votes-meter__value', item)
                        })

                    except:
                        reload(self.get_page_data())

                counter += 1
            return data

        except(req.RequestException, ValueError):
            print('Server error!')
        return False

    def check_info(self, tag_1, tag_2, item):
        titles = item.find(tag_1, class_=tag_2)
        if titles:
            titles = titles.get_text(strip=True)
        else:
            titles = "0"
        return titles


if __name__ == "__main__":
    news = ParserStat()
    print(news.get_page_data())
