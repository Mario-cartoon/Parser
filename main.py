from bs4 import BeautifulSoup
import requests as req
import json

class ParserStat:
    def __init__(self):
        self.url = 'https://habr.com/ru/users/newtechaudit/posts/page'

    def get_info(self):
        counter = 1
        data = {}
        data['info'] = []

        try:
            while(True):
                #print(self.url + str(counter))
                res = req.get(self.url + str(counter))
                soup = BeautifulSoup(res.text, 'html.parser')
                page = soup.find('a', class_='tm-pagination__navigation-link tm-pagination__navigation-link_active')
                items = soup.find_all('article', class_='tm-articles-list__item')

                if page == None:
                    break

                counter += 1

                for item in items:
                    data['info'].append({
                        'titles': item.find('a', class_='tm-article-snippet__title-link').get_text(strip=True),
                        'times': item.find('span', class_='tm-article-snippet__datetime-published').get_text(strip=True),
                        'views': item.find('span', class_='tm-icon-counter__value').get_text(strip=True),
                        'saved': item.find('span', class_='bookmarks-button__counter').get_text(strip=True),
                        'karma': item.find('span', class_='tm-votes-meter__value').get_text(strip=True)

                    })

            with open('data.txt', 'w') as outfile:
                json.dump(data, outfile, sort_keys=False, indent=2, ensure_ascii=False)
            return data
        except(req.RequestException, ValueError):
            print('Server error!')
        return False

if __name__ == "__main__":
    news = ParserStat()
    print(news.get_info())