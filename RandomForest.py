__author__ = 'andrewa'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import sklearn.ensemble
from sklearn.feature_extraction.text import CountVectorizer
import operator

dataframe_dict = {'alexa': [], 'conficker': [], 'cryptolocker': [], 'zeus': [], 'pushdo': [], 'rovnix': [], 'tinba': [],
                  'matsnu': [], 'ramdo': []}

word_dataframe = pd.read_csv('help/words.txt', names=['word'], header=None, dtype={'word': np.str}, encoding='utf-8')
word_dataframe = word_dataframe[word_dataframe['word'].map(lambda x: str(x).isalpha())]
word_dataframe = word_dataframe.applymap(lambda x: str(x).strip().lower())
word_dataframe = word_dataframe.dropna()
word_dataframe = word_dataframe.drop_duplicates()

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

all_domains = pd.concat([dataframe_dict['alexa'], dataframe_dict['conficker'], dataframe_dict['cryptolocker'],
                         dataframe_dict['zeus'], dataframe_dict['pushdo'], dataframe_dict['rovnix'],
                         dataframe_dict['tinba'], dataframe_dict['matsnu'], dataframe_dict['ramdo']],
                        ignore_index=True)

all_domains['length'] = [len(x) for x in all_domains['domain']]

import math
from collections import Counter


def entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count / lns * math.log(count / lns, 2) for count in p.values())

all_domains['entropy'] = [entropy(x) for x in all_domains['domain']]

alexa_vc = CountVectorizer(analyzer='char', ngram_range=(3, 5), min_df=1e-4, max_df=1.0)
counts_matrix = alexa_vc.fit_transform(dataframe_dict['alexa']['domain'])
alexa_counts = np.log10(counts_matrix.sum(axis=0).getA1())

dict_vc = CountVectorizer(analyzer='char', ngram_range=(3,5), min_df=1e-5, max_df=1.0)
counts_matrix = dict_vc.fit_transform(word_dataframe['word'])
dict_counts = np.log10(counts_matrix.sum(axis=0).getA1())

all_domains['alexa_grams'] = alexa_counts * alexa_vc.transform(all_domains['domain']).T
all_domains['word_grams'] = dict_counts * dict_vc.transform(all_domains['domain']).T
all_domains['diff'] = all_domains['alexa_grams'] - all_domains['word_grams']

#cond = all_domains['class'] == 'conficker'
#dga = all_domains[cond]
#legit = all_domains[~cond]
#plt.scatter(legit['length'], legit['alexa_grams'], s=120, c='#aaaaff', label='Alexa', alpha=.1)
#plt.scatter(dga['length'], dga['alexa_grams'], s=40, c='r', label='DGA', alpha=.3)
#plt.legend()
#pylab.xlabel('Domain Length')
#pylab.ylabel('Alexa NGram Matches')

weird_cond = (all_domains['class']=='legit') & (all_domains['word_grams']<3) & (all_domains['alexa_grams']<2)
weird = all_domains[weird_cond]
all_domains.loc[weird_cond, 'class'] = 'weird'
not_weird = all_domains[all_domains['class'] != 'weird']
X = not_weird.as_matrix(['length', 'entropy', 'alexa_grams', 'word_grams'])
y = np.array(not_weird['class'].tolist())

#X = all_domains.as_matrix(['length', 'entropy'])
#y = np.array(all_domains['class'].tolist())

clf = sklearn.ensemble.RandomForestClassifier(n_estimators=20)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

clf.fit(X, y)
scores = sklearn.cross_validation.cross_val_score(clf, X, y, cv=5, n_jobs=4)
print scores.mean()
#all_domains.boxplot('entropy', 'class')


#clf = sklearn.ensemble.RandomForestClassifier(n_estimators=20)
#scores = sklearn.cross_validation.cross_val_score(clf, X, y, cv=5, n_jobs=4)
#print scores.mean()