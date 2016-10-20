# coding:utf-8
import json, codecs
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
words = [u"кусок", u'ложь', u'исчезнуть', u'далёкий', u'начинаться', u'защищать', u'гаснуть', u'алый', u'стадо',
         u'засовывать', u'крик', u'шум', u'красть', u'понять', u'перестать', u'прошлый']

f = codecs.open('jaccard.json', 'r', 'utf-8')
jaccard_rows = json.loads(f.read())
#jaccard_rows = {}


def jaccard(s1, s2):
    s1 = set(s1)
    s2 = set(s2)
    return len(s1 & s2) / len(s1 | s2)


def read_rows():
    synrows = {}
    with open('synrows') as f:
        for line in f:
            line = line.strip()
            words = line.split(',')
            if words[0] == 'русский':
                row = words[1]
                synrows[row] = {'rus': words[2:]}
            elif words[0] == 'французский':
                synrows[row]['fr'] = words[1:]
            elif words[0] == 'английский':
                synrows[row]['eng'] = words[1:]
    return synrows


def elicit_fr():
    fr_model = gensim.models.Word2Vec.load('french_500_win10_sg.model')
    fr_model.init_sims(replace=True)
    for row in synrows:
        try:
            fr_main = synrows[row]['fr'][0].replace(' ', '_')
            fr_row = [x.replace(' ', '_') for x in synrows[row]['fr'][1:]]
            fr_synonyms = [s[0] for s in fr_model.most_similar(fr_main, topn=10)]
            j = jaccard(synrows[row]['fr'][1:], fr_synonyms[:len(fr_row)])
            jaccard_rows[row]['fr'] = [j, fr_synonyms]
        except KeyError:
            continue


def elicit_ru():
    rus_model = gensim.models.Word2Vec.load_word2vec_format('ruwikiruscorpora.model.bin.gz', binary=True)
    rus_model.init_sims(replace=True)
    for main in words:
        print(main)
        #try:
        row = synrows[main]['rus']
        print('row', row)
        ru_synonyms = [s[0] for s in rus_model.most_similar(main, topn=10)]
        print('syns', ru_synonyms)
        j = jaccard(synrows[main]['fr'][1:], ru_synonyms[:len(row)])
        print(j)
        jaccard_rows[main] = {'ru': [j, ru_synonyms]}
        #except KeyError:
         #   continue


def elicit_en():
    bnc_model = gensim.models.Word2Vec.load_word2vec_format('bnc.bin.gz', binary=True)
    bnc_model.init_sims(replace=True)
    for row in synrows:
        try:
            en_main = synrows[row]['eng'][0].replace(' ', '_')
            en_row = [x.replace(' ', '_') for x in synrows[row]['eng'][1:]]
            en_synonyms = [s[0] for s in bnc_model.most_similar(en_main, topn=10)]
            j = jaccard(synrows[row]['eng'][1:], en_synonyms[:len(en_row)])
            jaccard_rows[row] = {'en': [j, en_synonyms]}
        except KeyError:
            continue



if __name__ == '__main__':
    with open('synrows.json', 'r') as f:
        synrows = json.loads(f.read())
    #elicit_en()
    elicit_fr()
    js = json.dumps(jaccard_rows, ensure_ascii=False)
    f = codecs.open('jaccard.json', 'w', 'utf-8')
    f.write(js)