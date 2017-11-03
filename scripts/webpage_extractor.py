"""
given an url, extract a list of sentences from the body/article part of the content of the url.
"""

import json
import requests
import urllib.parse
import sys
import logging
import logging.config
import argparse
from bs4 import BeautifulSoup
import re

class WebPageExtractor:

    def __init__(self):
        self.logger = logging.getLogger()

    def get_content(self, url):
        """
            get the html code (in text) given an url.
        """
        self.logger.info("")
        # heades coming from a chromium requests of the api
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/61.0.3163.79 Chrome/61.0.3163.79 Safari/537.36'
        }
        self.logger.debug("url: " + url)

        resp = requests.get(url, headers = headers)
        self.logger.debug("status_code: " + str(resp.status_code))
        self.logger.debug("body: " + resp.text)

        assert resp.status_code == 200
        return resp.content

    def split_paragraph_sentences(self, paragraph):
        """
            split a paragraph into a list of sentences
            ex: split_paragraph_sentences("This is test. First test")
            return ["This is test", "First test"]
        """
        self.logger.info("")
        self.logger.debug(paragraph)

        # split by ponctuation
        l = re.split('[.!?]', paragraph)

        # filter list from empty string
        filtered_list = [x for x in l if x != "" and x != ' ']

        # use a set to remove duplicates
        self.logger.debug('result:' + str(filtered_list))
        return filtered_list

    def extract(self, soup, symbol):
        """
            extract from a soup (html.parser) all sentences for a given symbol html balise
            ex: extract(BeautifulSoup("<h1> C'est un test. test1 <h1/>", htmp.parser), h1)
            return ["C'est un test", "test1"]
        """
        l = []
        for paragraph in soup.body.find_all(symbol):
            l = l + self.split_paragraph_sentences(paragraph.get_text())

        return l

    def extract_sentences(self, content):
        self.logger.info("")
        soup = BeautifulSoup(content, 'html.parser')
        # extract from titles
        l = self.extract(soup, 'h1')
        l = l + self.extract(soup, 'h2')
        l = l + self.extract(soup, 'h3')
        l = l + self.extract(soup, 'p')

        # remove duplicates
        res = list(set(l))

        self.logger.debug(res)
        return res

    def proceed(self, url):
        self.logger.info(url)
        content = self.get_content(url)
        l = self.extract_sentences(content)

        self.logger.info(str(len(l)) + " sentences extracted.")
        if len(l) == 0:
            self.logger("0 sentence extracted from " + url)
        return l

if __name__ == "__main__":

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store',
        choices=['INFO', 'WARNING', 'ERROR', 'DEBUG'], default='ERROR',
        help='verbose: INFO, WARNING, ERROR, DEBUG')
    parser.add_argument('-u', '--url', dest='url', action='store',
        help='url to parse.', required=True)

    args = parser.parse_args()

    # set logging level
    logging.config.fileConfig('conf/logging.conf')
    verbose = getattr(args, 'verbose')
    if verbose == 'INFO':
        logging.getLogger().setLevel(logging.INFO)
    elif verbose == 'WARNING':
        logging.getLogger().setLevel(logging.WARNING)
    elif verbose == 'ERROR':
        logging.getLogger().setLevel(logging.ERROR)
    elif verbose == 'DEBUG':
        logging.getLogger().setLevel(logging.DEBUG)
        print(verbose)

    # get url
    url = getattr(args, 'url')

    # extract list of url
    extractor = WebPageExtractor()
    l = extractor.proceed(url)
    print(l)


        
        
        
        

    

