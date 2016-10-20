# coding: utf-8

import csv, json, codecs

HEADER = ('row', 'ru_Jaccard', 'ru_lex', 'ru_comp', 'fr_Jaccard', 'fr_lex', 'fr_comp', 'en_Jaccard', 'en_lex', 'en_comp')
with open('dsm_synonyms.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';', quotechar='"')
    writer.writerow(HEADER)

    synrows = json.loads(codecs.open('synrows.json', 'r', 'utf-8').read())
    jaccard = json.loads(codecs.open('jaccard.json', 'r', 'utf-8').read())
    for s in synrows:
        r_name = s
        try:
            row = (
            r_name, jaccard[s]['ru'][0], ', '.join(synrows[s]['rus']), ', '.join(jaccard[s]['ru'][1]),
            jaccard[s]['fr'][0], ', '.join(synrows[s]['fr']), ', '.join(jaccard[s]['fr'][1]),
            jaccard[s]['en'][0], ', '.join(synrows[s]['eng']), ', '.join(jaccard[s]['en'][1]),
            )
            writer.writerow(row)
        except:
            continue