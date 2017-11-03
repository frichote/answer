(work in progress)
Author: Eric Frichot
Date: 15/10/2017
Email: eric.frichot@gmail.com

# Purpose
Extract an answer from a web search. 
Ex: "Temps de cuisson pommes de terres"
Answer: 35 minutes au four...

# steps:

## Done:
- call qwant API as a web search from a sentence 
- extract sentences from a web page. 
- clean a sentence (remove stop words).

## Todo:
- clean the list of stop words.
- extract a list of synonym of a word from the web.
- order the list of extracted sentences by interest for the question.
-- create a score.
-- info which type of information is searched (time, location, duration).
-- return a list of result if several answers are availabe (ex: au four, à la poêle).

# installation

Done with python3.4.3.

dependencies: 're', 'argparse', 'logging', 're', 'unidecode', 'json', 'requests', 'sys', 'urllib', 'bs4' 

Use scripts from the home of the project.

# Description

## conf/
- logging.conf: global logging config

## data/
- stop_words.txt: list of stop words.

## scripts/
- clean_sentence.py: clean a sentence from accent, special characters and stop words
Ex: python3 scripts/clean_sentence.py -s " test 
à poUr" 

- qwant_extractor.py: extract a list of 10 qwant answer urls from a sentence. 
Ex: python3 scripts/qwant_extractor.py -s "Temps de cuisson pommes de terres"

- webpage_extractor.py: extract a list of sentences from the body of a webpage given an url.
Ex: python3 scripts/webpage_extractor.py -u https://www.tempsdecuisson.net/les-legumes-et-feculents/pomme-de-terre
