# coding: utf-8

import nltk, re
from nltk.corpus import stopwords
stop = set(stopwords.words('french'))
import string
punct = list(string.punctuation)
punct.remove("'")
punct.remove('-')
punct.append('«')
punct.append('»')
import treetaggerwrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')


def clean(text):
    book = re.search('(.*)\*?\*?\*? ?END OF TH', text, flags=re.U | re.DOTALL | re.I).group(1)
    book = re.sub('<[^>]*>', '', book, flags=re.DOTALL)
    if '*** START OF TH' in book or '***START OF TH':
        book = re.search('.*START OF TH.*?\*?\*?\*?(.*)', book, flags=re.U | re.DOTALL).group(1)
        if book is None:
            return None
        book = re.sub('Produced by.*?This file was produced from\\s+images\\s+generously\\s+made\\s+available by[^\n]*',
                      '', book, flags=re.DOTALL)
        # print(book)
    return book


def split_sent(text):
    # chargement du tokenizer
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/french.pickle')
    sentences = tokenizer.tokenize(text.replace('\n', ' ').replace('&mdash;', ''))
        #"Jadis, une nuit, je fus un papillon, voltigeant, content de son sort. Puis, je m’éveillai, étant Tchouang-tseu. Qui suis-je en réalité ? Un papillon qui rêve qu’il est Tchouang-tseu ou Tchouang qui s’imagine qu’il fut papillon ?")

    for sent in sentences:
        if len(sent) > 10:
            sent = sent.strip(' ').lower()
            for p in punct:
                sent = sent.replace(p, '')
            #for s in stop:
            #    sent = re.sub('\b{}\b'.format(s), '', sent)
            sent = re.sub('\s+', ' ', sent)
            tags = tagger.tag_text(sent)
            # do something now!
            fr.write(sent + '\n')

fr = open('french_gut3.txt', 'w', encoding='utf-8')
fr_files = set()
with open('french.txt') as f:
    for line in f:
        line = line.strip()
        fr_files.add(line)

for f in fr_files:
    print(f)
    if len(f) < 10:
        continue
    try:
        with open('./gutenberg/' + f) as fr_text:
            text = fr_text.read()
    except UnicodeDecodeError:
        with open('./gutenberg/' + f, encoding='iso-8859-1') as fr_text:
            text = fr_text.read()
    clean_t = clean(text)
    #print(clean_t)
    split_sent(clean_t)
fr.close()
