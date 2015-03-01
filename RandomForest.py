__author__ = 'andrewa'
import pandas as pd
import numpy as np

dataframe_dict = {'alexa': [], 'conficker': [], 'cryptolocker': [], 'zeus': [], 'pushdo': [],
                  'goz': [], 'new_goz': [], 'others_dga': [], 'rovnix': [], 'tinba': [],
                  'matsnu': [], 'ramdo': []}
for i, v in dataframe_dict.iteritems():
    if i == 'alexa':
        v = pd.read_csv('all_legit.txt', names=['uri'], header=None, encoding='utf-8')
        v['domain'] = v.applymap(lambda x: x.split('.')[0].strip().lower())
        del v['uri']
        v['class'] = 'legit'
        dataframe_dict[i] = v
    else:
        v = pd.read_csv('dga_wordlists/' + i + '.txt', names=['uri'], header=None, encoding='utf-8')
        v['domain'] = v.applymap(lambda x: x.split('.')[0].strip().lower())
        del v['uri']
        v['class'] = i
        dataframe_dict[i] = v

print '# done parsing'

all_domains = pd.concat([dataframe_dict['alexa'], dataframe_dict['conficker'], dataframe_dict['cryptolocker'], \
                         dataframe_dict['zeus'], dataframe_dict['pushdo'], dataframe_dict['goz'], \
                         dataframe_dict['new_goz'], dataframe_dict['others_dga'], dataframe_dict['rovnix'], \
                         dataframe_dict['tinba'], dataframe_dict['matsnu'], dataframe_dict['ramdo']], \
                        ignore_index=True)

all_domains['length'] = [len(x) for x in all_domains['domain']]

import math
from collections import Counter


def entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count / lns * math.log(count / lns, 2) for count in p.values())


all_domains['entropy'] = [entropy(x) for x in all_domains['domain']]

X = all_domains.as_matrix(['length', 'entropy'])
y = np.array(all_domains['class'].tolist())

print y
import sklearn.ensemble

clf = sklearn.ensemble.RandomForestClassifier(n_estimators=20)
scores = sklearn.cross_validation.cross_val_score(clf, X, y, cv=5, n_jobs=4)
print scores
