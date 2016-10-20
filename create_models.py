# coding: utf-8

import sys
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

argument = 'french_gut2.txt'

# создаём структуру данных для модели
data = gensim.models.word2vec.LineSentence(argument)

# инициализируем модель (параметры в скобочках: data - данные, size - размер вектора, window -размер окна наблюдения,
#                                               min_count - мин. частотность слова в корпусе, которое мы берем,
#                                               sg - используемый алгоритм обучение (0 - CBOW, 1 - Skip-gram))
model = gensim.models.Word2Vec(data, size=500, window=5, min_count=2, sg=0)
# чтобы модель использовала меньше RAM (но теперь её нельзя менять!)
model.init_sims(replace=True)

# сохраняем
model.save('french_500_win10_cbow.model')