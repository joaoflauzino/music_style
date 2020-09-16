from bs4 import BeautifulSoup
import requests
import pandas as pd

class Collect:

    def __init__(self, url):
        self.url = url

    def get_style(self):
        page = requests.get('https://www.vagalume.com.br/browse/style/')
        soup = BeautifulSoup(page.content, 'html.parser')
        category = soup.find("ul", {"class": "xsList3 xsmList4 smList5 mdList5 gridList flexSpcStart"})
        itens = category.find_all("li")
        categorys = []
        links = []
        for aTag in itens:
            links.append(aTag.find("a")['href'])
            categorys.append(aTag.find("p", {"class": "w1 itemTitle"}).getText())
        return links, categorys

        

    def get_authors(self, links, categorys):
        dataset = []
        for link in range(len(links)):
            pg = requests.get(self.url + links[link])
            soup2 = BeautifulSoup(pg.content, 'html.parser')
            authors = soup2.find_all('ul', {'class': 'xsList2 smList3 mdList6 gridList'})
            singers = authors[1].find_all('li')
        
            for sing in singers:
                raw = []
                raw.append(sing.find("a")['href'])
                raw.append(sing.find("p", {"class": "h22 w1 itemTitle"}).getText())
                raw.append(categorys[link])
                raw.append(links[link])
                dataset.append(raw)

        return pd.DataFrame(dataset, columns = ["singer", "singer_link", "category", "category_link"])


    





        



