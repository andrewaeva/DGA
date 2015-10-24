__author__ = 'andrewa'
import pandas as pd
import numpy as np

dataframe_dict = {'alexa': [], 'conficker': [], 'cryptolocker': [], 'zeus': [], 'pushdo': [], 'rovnix': [], 'tinba': [],
                  'matsnu': [], 'ramdo': []}

for i, v in dataframe_dict.iteritems():
    if i == 'alexa':
        v = pd.read_csv('../all_legit.txt', names=['uri'], header=None, encoding='utf-8')
        v['domain'] = v.applymap(lambda x: x.split('.')[0].strip().lower())
        del v['uri']
        v['class'] = 'legit'
        dataframe_dict[i] = v
    else:
        v = pd.read_csv('../dga_wordlists/' + i + '.txt', names=['uri'], header=None, encoding='utf-8')
        v['domain'] = v.applymap(lambda x: x.split('.')[0].strip().lower())
        del v['uri']
        v['class'] = 'dga'
        dataframe_dict[i] = v

for i in ['alexa', 'conficker', 'cryptolocker', 'zeus', 'pushdo', 'rovnix', 'tinba', 'matsnu', 'ramdo']:
    rows = np.random.choice(dataframe_dict[i].index, 1000)
    f = open('1000domains/'+i+'_1000.txt', 'w')
    for j in dataframe_dict[i]['domain'][rows]:
        f.write(str(j+'\n'))
    f.close()
