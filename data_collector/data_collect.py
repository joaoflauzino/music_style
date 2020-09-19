from bs4 import BeautifulSoup
import requests
import pandas as pd

class Collect:

    def __init__(self, url):
        self.url = url

    def scraper(self):
        page = requests.get(self.url + '/browse/style/')
        soup = BeautifulSoup(page.content, 'html.parser')
        category = soup.find("ul", {"class": "xsList3 xsmList4 smList5 mdList5 gridList flexSpcStart"})
        itens = category.find_all("li")
        categorys = []
        links = []
        for aTag in itens:
            links.append(aTag.find("a")['href'])
            categorys.append(aTag.find("p", {"class": "w1 itemTitle"}).getText())

        dataset = []
        
        for link in range(len(links)):
            pg = requests.get(self.url + links[link])
            soup2 = BeautifulSoup(pg.content, 'html.parser')
            authors = soup2.find_all('ul', {'class': 'xsList2 smList3 mdList6 gridList'})
            singers = authors[1].find_all('li')
        
            for sing in singers:
                request = self.url + sing.find("a")['href']
                pg_letters = requests.get(request)
                soup3 = BeautifulSoup(pg_letters.content, 'html.parser')
                letters = soup3.find_all('ol', {'id': 'topMusicList'})
                for let in letters:
                    for k in let.find_all('li'):
                        raw = []
                        raw.append(sing.find("p", {"class": "h22 w1 itemTitle"}).getText())
                        raw.append(sing.find("a")['href'])
                        raw.append(categorys[link])
                        raw.append(links[link])
                        raw.append(k.find("a").getText())
                        raw.append(k.find("a")['href'])
                        pg_l = requests.get(self.url + k.find("a")['href'])
                        soup4 = BeautifulSoup(pg_l.content, 'html.parser')
                        raw.append(str(soup4.find_all('div', {'id': 'lyrics'})[0]))
                        try:
                            raw.append(soup4.find_all('a', {'class': 'h16'})[3].getText())
                        except:
                            raw.append('')
                        dataset.append(raw)

        import pdb; pdb.set_trace()
                        
        pd.DataFrame(dataset, columns = ["singer", "singer_link", "category", "category_link", "music_name", "music_link", "lyrics", "is_pt"]).to_pickle('input/songs.pkl')


        



