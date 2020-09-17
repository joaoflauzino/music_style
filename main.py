from data_collector.data_collect import Collect

if __name__ == "__main__":

    collector = Collect('http://www.vagalume.com.br')
    collector.scraper()