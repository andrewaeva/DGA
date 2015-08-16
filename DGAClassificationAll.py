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
        v['class'] = 'dga'
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

# all_domains.boxplot('length','class')
# pylab.ylabel('Domain Length')
# all_domains.boxplot('entropy','class')
# pylab.ylabel('Domain Entropy')

# cond = all_domains['class'] != 'legit'
# dga = all_domains[cond]
# alexa = all_domains[~cond]
# plt.scatter(alexa['length'], alexa['entropy'], s=140, c='r', label='Legit', alpha=.4)
# plt.scatter(dga['length'], dga['entropy'], s=140, c='#aaaaff', label='DGA', alpha=.4)
# plt.legend()
# pylab.xlabel('Domain Length')
# pylab.ylabel('Domain Entropy')
# plt.show()


alexa_vc = CountVectorizer(analyzer='char', ngram_range=(3, 5), min_df=1e-4, max_df=1.0)
counts_matrix = alexa_vc.fit_transform(dataframe_dict['alexa']['domain'])
alexa_counts = np.log10(counts_matrix.sum(axis=0).getA1())

dict_vc = CountVectorizer(analyzer='char', ngram_range=(3, 5), min_df=1e-5, max_df=1.0)
counts_matrix = dict_vc.fit_transform(word_dataframe['word'])
dict_counts = np.log10(counts_matrix.sum(axis=0).getA1())

all_domains['alexa_grams'] = alexa_counts * alexa_vc.transform(all_domains['domain']).T
all_domains['word_grams'] = dict_counts * dict_vc.transform(all_domains['domain']).T
all_domains['diff'] = all_domains['alexa_grams'] - all_domains['word_grams']

print 'Done data'


# cond = all_domains['class'] != 'legit'
# dga = all_domains[cond]
# legit = all_domains[~cond]
# plt.scatter(legit['length'], legit['word_grams'],  s=140, c='r', label='legit', alpha=.1)
# plt.scatter(dga['length'], dga['word_grams'], s=140, c='#aaaaff', label='DGA', alpha=.1)
# plt.legend()
# pylab.xlabel('Domain Length')
# pylab.ylabel('Dictionary NGram Matches')
# plt.show()

# cond = all_domains['class'] != 'legit'
# dga = all_domains[cond]
# legit = all_domains[~cond]
# plt.scatter(legit['length'], legit['diff'], s=140, c='r', label='Legit', alpha=.4)
# plt.scatter(dga['length'], dga['diff'], s=140, c='#aaaaff', label='DGA', alpha=.4)
# plt.legend()
# pylab.xlabel('Domain Length')
# pylab.ylabel('Diff')
# plt.show()

# weird_cond = (all_domains['class']=='legit') & (all_domains['word_grams']<3) & (all_domains['alexa_grams']<2)
# weird = all_domains[weird_cond]
# all_domains.loc[weird_cond, 'class'] = 'weird'
# not_weird = all_domains[all_domains['class'] != 'weird']
# X = not_weird.as_matrix(['length', 'entropy', 'alexa_grams', 'word_grams'])
# y = np.array(not_weird['class'].tolist())

X = all_domains.as_matrix(['length', 'entropy', 'alexa_grams', 'word_grams', 'diff'])
y = np.array(all_domains['class'].tolist())

from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import ExtraTreesClassifier

from sklearn.cross_validation import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf1 = LogisticRegression(random_state=1)
clf1.fit(X_train, y_train)
clf2 = RandomForestClassifier(bootstrap=True, max_depth=None, class_weight="auto", min_samples_leaf=1,
                              min_samples_split=1, n_estimators=1500, n_jobs=40, oob_score=False,
                              random_state=1, verbose=1)
clf2.fit(X_train, y_train)
clf3 = GaussianNB()
clf3.fit(X_train, y_train)
clf4 = ExtraTreesClassifier()
clf4.fit(X_train, y_train)

eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3), ('etr', clf4)], voting='soft')

for clf, label in zip([clf1, clf2, clf3, clf4, eclf], ['Logistic Regression', 'Random Forest', 'naive Bayes',
                                                       'Extra Tree', 'Ensemble']):
    scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5, scoring='accuracy')
    print("Accuracy: %0.6f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

from sklearn.metrics import confusion_matrix
y_pred = clf2.predict(X_test)
labels = ['legit', 'dga']
cm = confusion_matrix(y_test, y_pred, labels)


def plot_cm(cm, labels):
    percent = (cm*100.0)/np.array(np.matrix(cm.sum(axis=1)).T)  # Derp, I'm sure there's a better way
    print 'Confusion Matrix Stats'
    for i, label_i in enumerate(labels):
        for j, label_j in enumerate(labels):
            print "%s/%s: %.2f%% (%d/%d)" % (label_i, label_j, (percent[i][j]), cm[i][j], cm[i].sum())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(b=False)
    cax = ax.matshow(percent, cmap='coolwarm')
    pylab.title('Confusion matrix of the classifier')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels)
    pylab.xlabel('Predicted')
    pylab.ylabel('True')
    pylab.show()


plot_cm(cm, labels)