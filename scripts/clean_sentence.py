"""
    clean a sentence. 
        - Remove special character.
        - remove accents.
        - remove stop words.
        - lower case
"""

import sys
import logging
import logging.config
import argparse
import unidecode
import re

class CleanSentence:

    def __init__(self):
        self.logger = logging.getLogger()

        # init stop words (TODO: list of stop words to clean). 
        with open("data/stop_words.txt") as f:
            content = f.readlines()
            self.stop_words = [x.strip() for x in content]

    def remove_accents(self, sentence):
        self.logger.info(sentence)
        res = unidecode.unidecode(sentence)
        self.logger.debug("result : " + res)
        return res 

    def remove_special_characters(self, sentence):
        """ 
            remove special characters and double spaces
        """
        self.logger.info(sentence)
        res = re.sub(r'[\t\n\r]', ' ', sentence).replace('  ', ' ')
        self.logger.debug("result : " + res)
        return res

    def remove_stop_words(self, sentence):
        self.logger.info(sentence)
        # remove stop words 
        res = " " + sentence + " " 
        for word in self.stop_words:
            res = res.replace(" " + word + " ", " ") 
        # remove double spaces
        res = res.replace('  ', ' ')
        # remove first space
        res = re.sub(r'^ ', '', res) 
        # remove last space
        res = re.sub(r' $', '', res) 
        self.logger.debug("result : " + res)
        return res
        
    def proceed(self, sentence):
        self.logger.info(sentence) 
        sentence = self.remove_special_characters(sentence)
        sentence = self.remove_accents(sentence)
        sentence = sentence.lower() 
        sentence = self.remove_stop_words(sentence) 
        return sentence

if __name__ == "__main__":

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', action='store',
        choices=['INFO', 'WARNING', 'ERROR', 'DEBUG'], default='ERROR',
        help='verbose: INFO, WARNING, ERROR, DEBUG')
    parser.add_argument('-s', '--sentence', dest='sentence', action='store',
        help='Sentence to clean (quote) ex:"test sentence"', required=True)

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
    extractor = CleanSentence()
    l = extractor.proceed(sentence)
    print(l)

