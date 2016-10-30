# coding: utf-8

import nltk
import string
punct = list(string.punctuation)
punct.remove("'")
punct.remove('-')
punct.append('«')
punct.append('»')
punct.append('…')
import treetaggerwrapper
import re

# CHANGE LANGUAGE
tagger = treetaggerwrapper.TreeTagger(TAGLANG='pl')

def french():
    tokenizer = nltk.data.load('tokenizers/punkt/PY3/polish.pickle')
    with open('wiki_pl.txt', 'r', encoding='utf-8') as f:
        with open('polish_wiki_tagged.txt', 'w', encoding='utf-8') as fr:
            for line in f:
                #print(line)
                sentences = tokenizer.tokenize(line.strip().replace('&mdash;', ''))
                for sent in sentences:
                    if len(sent) > 10:
                        sent = sent.strip(' ').lower()
                        for p in punct:
                            sent = sent.replace(p, '')
                        # for s in stop:
                        #    sent = re.sub('\b{}\b'.format(s), '', sent)
                        sent = re.sub('\s+', ' ', sent)
                        tags = tagger.tag_text(sent)
                        sent = ' '.join([tag.split('\t')[-1] + '_' + tag.split('\t')[1].split(':')[0] for tag in tags])
                        # do something now!
                        fr.write(sent + '\n')


if __name__ == '__main__':
    # CHANGE FUNCTION
    french()