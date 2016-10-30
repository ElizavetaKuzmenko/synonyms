# coding: utf-8

import nltk, re
#from nltk.corpus import stopwords

# CHANGE STOPWORDS
#stop = set(stopwords.words('french'))
import string
punct = list(string.punctuation)
punct.remove("'")
punct.remove('-')
punct.append('«')
punct.append('»')
punct.append('…')
import treetaggerwrapper

# CHANGE LANGUAGE
tagger = treetaggerwrapper.TreeTagger(TAGLANG='pl')

# OPEN CORRECT FILE FOR WRITING
#fr = open('french_gut3.txt', 'w', encoding='utf-8')
#it = open('italian_gut.txt', 'w', encoding='utf-8')
#de = open('german_gut.txt', 'w', encoding='utf-8')
pl = open('polish_gut.txt', 'w', encoding='utf-8')


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


def split_sent_fr(text):
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
            sent = ' '.join([tag.split('\t')[-1] + '_' + tag.split('\t')[1].split(':')[0] for tag in tags])
            # do something now!
            fr.write(sent + '\n')


def split_sent_pl(text):
    # chargement du tokenizer
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/polish.pickle')
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
            sent = ' '.join([tag.split('\t')[-1] + '_' + tag.split('\t')[1].split(':')[0] for tag in tags])
            # do something now!
            pl.write(sent + '\n')


def split_sent_it(text):
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/italian.pickle')
    sentences = tokenizer.tokenize(text.replace('\n', ' ').replace('&mdash;', ''))

    for sent in sentences:
        if len(sent) > 10:
            sent = sent.strip(' ').lower()
            for p in punct:
                sent = sent.replace(p, '')
            # for s in stop:
            #    sent = re.sub('\b{}\b'.format(s), '', sent)
            sent = re.sub('\s+', ' ', sent)
            tags = tagger.tag_text(sent)
            sent = ' '.join([tag.split('\t')[-1].split('|')[0] + '_' + tag.split('\t')[1].split(':')[0] for tag in tags]).replace('@card@_NUM', '').replace('—_NOM', '')
            # do something now!
            it.write(sent + '\n')


def split_sent_de(text):
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/german.pickle')
    sentences = tokenizer.tokenize(text.replace('\n', ' ').replace('&mdash;', ''))

    for sent in sentences:
        if len(sent) > 10:
            sent = sent.strip(' ').lower()
            for p in punct:
                sent = sent.replace(p, '')
            # for s in stop:
            #    sent = re.sub('\b{}\b'.format(s), '', sent)
            sent = re.sub('\s+', ' ', sent)
            tags = tagger.tag_text(sent)
            sent = ' '.join([tag.split('\t')[-1] + '_' + tag.split('\t')[1].split(':')[0] for tag in tags]).replace('_$', '').replace('@card@_CARD', '')
            # do something now!
            de.write(sent + '\n')


def load_fr():
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
            with open('./gut/' + f) as fr_text:
                text = fr_text.read()
        except UnicodeDecodeError:
            with open('./gut/' + f, encoding='iso-8859-1') as fr_text:
                text = fr_text.read()
        clean_t = clean(text)
        #print(clean_t)
        split_sent_fr(clean_t)
    fr.close()


def load_pl():
    pl_files = set()
    with open('polish.txt') as f:
        for line in f:
            line = line.strip()
            pl_files.add(line)

    for f in pl_files:
        print(f)
        if len(f) < 10:
            continue
        try:
            with open('./gutenberg/' + f) as pl_text:
                text = pl_text.read()
        except UnicodeDecodeError:
            with open('./gutenberg/' + f, encoding='iso-8859-1') as pl_text:
                text = pl_text.read()
        clean_t = clean(text)
        #print(clean_t)
        split_sent_pl(clean_t)
    pl.close()


def load_it():
    it_files = set()
    with open('italian.txt') as f:
        for line in f:
            line = line.strip()
            it_files.add(line)

    for f in list(it_files):
        print(f)
        if len(f) < 10:
            continue
        try:
            with open('./gutenberg/' + f) as it_text:
                text = it_text.read()
        except UnicodeDecodeError:
            with open('./gutenberg/' + f, encoding='iso-8859-1') as it_text:
                text = it_text.read()
        clean_t = clean(text)
        # print(clean_t)
        split_sent_it(clean_t)
    it.close()


def load_de():
    de_files = set()
    with open('german.txt') as f:
        for line in f:
            line = line.strip()
            de_files.add(line)

    for f in list(de_files):
        print(f)
        if len(f) < 10:
            continue
        try:
            with open('./gutenberg/' + f) as de_text:
                text = de_text.read()
        except UnicodeDecodeError:
            with open('./gutenberg/' + f, encoding='iso-8859-1') as de_text:
                text = de_text.read()
        clean_t = clean(text)
        # print(clean_t)
        split_sent_de(clean_t)
    de.close()



if __name__ == '__main__':
    # CHANGE INTO CORRECT FUNCTION
    load_pl()
