import os

texts = set()
with open('texts.txt') as f:
    for line in f:
        line = line.strip()
        if line != '':
            texts.add(line)

print(len(texts))
files = os.listdir('./gutenberg')
for f in files:
    if f not in texts:
        print(f)
        #with open('./gutenberg/' + f) as ff:
        #    text = ff.read()
        #    if 'Language: English' in text:
        #        print('English', f)
        #    else:
        #        print(f)