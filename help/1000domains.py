__author__ = 'andrewa'
import pandas as pd
import numpy as np

dataframe_dict = {'alexa': [], 'conficker': [], 'cryptolocker': [], 'zeus': [], 'pushdo': [], 'rovnix': [], 'tinba': [],
                  'matsnu': [], 'ramdo': []}

for i, v in dataframe_dict.iteritems():
    if i == 'alexa':
        v = pd.read_csv('../all_legit.txt', names=['uri'], header=None, encoding='utf-8')
        v['domain'] = v.applymap(lambda x: x.split(" ")[0].strip().lower())
        del v['uri']
        v['class'] = 'legit'
        dataframe_dict[i] = v
    else:
        v = pd.read_csv('../dga_wordlists/' + i + '.txt', names=['uri'], header=None, encoding='utf-8')
        v['domain'] = v.applymap(lambda x: x.strip().lower())
        del v['uri']
        v['class'] = i
        dataframe_dict[i] = v

for i in ['alexa', 'conficker', 'cryptolocker', 'zeus', 'pushdo', 'rovnix', 'tinba', 'matsnu', 'ramdo']:
    rows = np.random.choice(dataframe_dict[i].index, 1000)
    if i == 'alexa':
        dataframe_dict[i] = dataframe_dict[i].sample(8000, axis=0, random_state=242)
    else:
        dataframe_dict[i] = dataframe_dict[i].sample(1000, axis=0, random_state=242)

all_domains = pd.concat([dataframe_dict['alexa'], dataframe_dict['conficker'], dataframe_dict['cryptolocker'],
                         dataframe_dict['zeus'], dataframe_dict['pushdo'], dataframe_dict['rovnix'],
                         dataframe_dict['tinba'], dataframe_dict['matsnu'], dataframe_dict['ramdo']],
                        ignore_index=True)
all_domains.to_csv("dataset_1000.csv", encoding='utf-8')
# print dataframe_dict[i]['domain', 'class'][rows]
# f = open('1000domains/rnn.txt', 'w')
# for j in dataframe_dict[i]['domain'][rows]:
#    f.write(str(j+'\n'))
# f.close()
