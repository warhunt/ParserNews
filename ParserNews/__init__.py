from os import system
from typing import List
from urllib.error import URLError
from urllib.request import urlopen
from urllib.parse import urljoin
from lxml.html import fromstring
import logging.config
from lxml import etree
import re
from pymongo.errors import OperationFailure
import sys

from ParserNews.config import ConfigFactory
from ParserNews.News import News
from ParserNews.database import init_db


class ParserNews:
    def __init__(self) -> None:
        """Constructor ParserNews"""
        config = ConfigFactory.factory()
        logging.config.dictConfig(config.LOGGING)
        self.__logger = logging.getLogger(config.LOGGER_NAME)
        self.__url_website = config.URL_WEBSITE

        init_db(**config.CONNECTION_TO_DB)

    def get_html(self):
        """Get html from website"""
        try:
            return fromstring(urlopen(self.__url_website).read().decode('cp1251', 'ignore'))
        except URLError:
            print('Url is not correct or server is not available')
            self.__logger.critical('Url is not correct or server is not available')

    def parse_news_from_html(self, html: str) -> List[News]:
        """Parse news from html"""
        if html is None:
            return []

        try:
            last_news = News.objects(news_from='ВА РБ').order_by('-date').first()
        except Exception as exs:
            self.__logger.critical(str(exs))
            self.__logger.info(f'---FINISH to parse news---')
            print(str(exs))
            sys.exit(1)    

        new_news_list=[]
        for index, elem in enumerate(html.cssselect('.seredina1_1 .seredina1_1')):
            try:
                news_link = None
                news_text = None
                news_date = None

                strong = elem.cssselect('strong')[0]
                if not len(strong.cssselect('a')):
                    date = html.cssselect('.verh1_1')[index]
                    news_date = date.cssselect('.verh1_1 div')[1].text
                    news_header = strong.text
                    news_text = elem.cssselect('p')

                    if len(elem.cssselect('a')):
                        news_link = elem.cssselect('a')[0].get('href')
                else:
                    a = strong.cssselect('a')[0]
                    new_doc = fromstring(urlopen(urljoin(self.__url_website, a.get('href'))).read().decode('cp1251', 'ignore'))

                    news_date = new_doc.cssselect('.headdate')[0].text
                    news_header = new_doc.cssselect('b')[0].text
                    news_text = new_doc.cssselect('p')

                    if len(new_doc.cssselect('a')):
                        news_link = new_doc.cssselect('a')[0].get('href')

                news_text_list = []
                for t in news_text:
                    etree.strip_tags(t, 'b', 'span', 'a')
                    t_clear = re.sub('[\\n\\b\\f\\r\\t\\v\\a]','', str(t.text)).strip()
                    news_text_list.append(t_clear)

                news_current_date = News.generate_corrent_date(news_date)

                new_news = News(
                    header=news_header,
                    date=news_current_date,
                    text=news_text_list
                )

                if news_link:
                    new_news.link = news_link

                self.__logger.info('News is parsed')
                print('News is parsed')

                if last_news and last_news.date == new_news.date:
                    self.__logger.info("It's an old news")
                    print("It's an old news")
                    break

                self.__logger.info("It's a new news")
                print("It's a new news")
                new_news_list.append(new_news)

            except Exception as exp:
                self.__logger.error('Error when try to parse news')
                print(f'Error when try to parse news: {str(exp)}')
                continue
    
        return new_news_list            

    def add_news_to_DB(self, news: List[News]) -> None:
        """Add news to db"""
        news_count = len(news)
        count = 0
        if not news_count == 0:
            for obj in news:
                try:
                    obj.save()
                    count += 1
                    self.__logger.info('News is added')
                    print('News is added')
                except:
                    self.__logger.error('News is not added')
                    print('News is not added')
        self.__logger.info(f'Added {count}/{news_count} news')        
            
    
    def work(self) -> None:
        """Main function to start parsing"""
        self.__logger.info(f'---START to parse news---')
        html = self.get_html()
        news = self.parse_news_from_html(html)
        self.add_news_to_DB(news)
        self.__logger.info(f'---FINISH to parse news---')