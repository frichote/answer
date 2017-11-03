"""
given a list of words, call qwant api for web search and extract the list of 10 url results
ex: 
https://api.qwant.com/api/search/web?count=10&device=desktop&extensionDisabled=true&safesearch=1&locale=cs_CZ&q=eric%20frichot&t=web
"""

import json
import requests
import urllib.parse
import sys
import logging
import logging.config
import argparse

class QwantExtractor:

    def __init__(self):
        self.logger = logging.getLogger()

    def build_url(self, sentence):
        self.logger.info("")
        base_url = "https://api.qwant.com/api/search/web?count=10&device=desktop&extensionDisabled=true&safesearch=1&locale=cs_CZ&t=web&q="
        encoded_sentence = urllib.parse.quote(sentence)
        url = base_url + encoded_sentence
        self.logger.debug("url:" + url)
        return url

    def call_qwant(self, url):
        self.logger.info("")
        # heades coming from a chromium requests of the api
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'api.qwant.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/61.0.3163.79 Chrome/61.0.3163.79 Safari/537.36'
        }
        self.logger.debug("url: " + url)

        resp = requests.get(url, headers = headers)
        self.logger.debug("status_code: " + str(resp.status_code))
        self.logger.debug("body: " + resp.text)

        assert resp.status_code == 200
        return resp.text

    def parse_response(self, text):
        self.logger.info("")
        js = json.loads(text)
        list_url = []
        if 'data' not in js or 'result' not in js['data'] or 'items' not in js['data']['result']:
            self.logger.error("response json not in expected format:" + text)

        for item in js['data']['result']['items']:
            if 'url' not in item:
                self.logger.error("item not in expected format:" + item)
            list_url.append(item['url'])   

        return list_url

    def proceed(self, sentence):
        self.logger.info(sentence) 
        url = self.build_url(sentence)
        text = self.call_qwant(url)
        return self.parse_response(text)

if __name__ == "__main__":

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store',
        choices=['INFO', 'WARNING', 'ERROR', 'DEBUG'], default='ERROR',
        help='verbose: INFO, WARNING, ERROR, DEBUG')
    parser.add_argument('-s', '--sentence', dest='sentence', action='store',
        help='Sentence for extraction (quote) ex:"test sentence"', required=True)

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

    # get sentence
    sentence = getattr(args, 'sentence')

    # extract list of url
    extractor = QwantExtractor()
    l = extractor.proceed(sentence)
    print(l)


        
        
        
        

    

