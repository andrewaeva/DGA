__author__ = 'andrewa'
import pandas as pd
import tldextract
import numpy as np
alexa_dataframe = pd.read_csv('all_legit.txt', names=['uri'], header=None, encoding='utf-8')
alexa_dataframe['domain'] = alexa_dataframe.applymap(lambda x: x.split('.')[0].strip().lower())
del alexa_dataframe['uri']
alexa_dataframe['class'] = 'legit'

conficker_data = pd.read_csv('dga_wordlists/conficker.txt', names=['uri'], header=None, encoding='utf-8')
conficker_data['domain'] = conficker_data.applymap(lambda x: x.split('.')[0].strip().lower())
del conficker_data['uri']
conficker_data['class'] = 'conficker'

cryptolocker_data = pd.read_csv('dga_wordlists/cryptolocker.txt', names=['uri'], header=None, encoding='utf-8')
cryptolocker_data['domain'] = cryptolocker_data.applymap(lambda x: x.split('.')[0].strip().lower())
del cryptolocker_data['uri']
cryptolocker_data['class'] = 'cryptolocker'

zeus_data = pd.read_csv('dga_wordlists/zeus.txt', names=['uri'], header=None, encoding='utf-8')
zeus_data['domain'] = zeus_data.applymap(lambda x: x.split('.')[0].strip().lower())
del zeus_data['uri']
zeus_data['class'] = 'zeus'

pushdo_data = pd.read_csv('dga_wordlists/pushdo.txt', names=['uri'], header=None, encoding='utf-8')
pushdo_data['domain'] = pushdo_data.applymap(lambda x: x.split('.')[0].strip().lower())
del pushdo_data['uri']
pushdo_data['class'] = 'pushdo'

goz_data = pd.read_csv('dga_wordlists/goz.txt', names=['uri'], header=None, encoding='utf-8')
goz_data['domain'] = goz_data.applymap(lambda x: x.split('.')[0].strip().lower())
del goz_data['uri']
goz_data['class'] = 'goz'

new_goz_data = pd.read_csv('dga_wordlists/new_goz.txt', names=['uri'], header=None, encoding='utf-8')
new_goz_data['domain'] = new_goz_data.applymap(lambda x: x.split('.')[0].strip().lower())
del new_goz_data['uri']
new_goz_data['class'] = 'new_goz'

others_dga_data = pd.read_csv('dga_detection/dga_domains.txt', names=['uri'], header=None, encoding='utf-8')
others_dga_data['domain'] = others_dga_data.applymap(lambda x: x.split('.')[0].strip().lower())
del others_dga_data['uri']
others_dga_data['class'] = 'others_dga'

rovnix_data = pd.read_csv('dga_wordlists/rovnix.txt', names=['uri'], header=None, encoding='utf-8')
rovnix_data['domain'] = rovnix_data.applymap(lambda x: x.split('.')[0].strip().lower())
del rovnix_data['uri']
rovnix_data['class'] = 'rovnix'

tinba_data = pd.read_csv('dga_wordlists/tinba.txt', names=['uri'], header=None, encoding='utf-8')
tinba_data['domain'] = tinba_data.applymap(lambda x: x.split('.')[0].strip().lower())
del tinba_data['uri']
tinba_data['class'] = 'tinba'

matsnu_data = pd.read_csv('dga_wordlists/matsnu.txt', names=['uri'], header=None, encoding='utf-8')
matsnu_data['domain'] = matsnu_data.applymap(lambda x: x.split('.')[0].strip().lower())
del matsnu_data['uri']
matsnu_data['class'] = 'matsnu'

ramdo_data = pd.read_csv('dga_wordlists/ramdo.txt', names=['uri'], header=None, encoding='utf-8')
ramdo_data['domain'] = ramdo_data.applymap(lambda x: x.split('.')[0].strip().lower())
del ramdo_data['uri']
ramdo_data['class'] = 'ramdo'

print '# done parsing'

all_domains = pd.concat([alexa_dataframe, conficker_data, cryptolocker_data, zeus_data,\
                         pushdo_data, goz_data, new_goz_data, others_dga_data, rovnix_data,\
                         tinba_data, matsnu_data, ramdo_data], ignore_index=True)

all_domains['length'] = [len(x) for x in all_domains['domain']]

import math
from collections import Counter

def entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

all_domains['entropy'] = [entropy(x) for x in all_domains['domain']]

X = all_domains.as_matrix(['length', 'entropy'])
y = np.array(all_domains['class'].tolist())

print y
import sklearn.ensemble
clf = sklearn.ensemble.RandomForestClassifier(n_estimators=20)
scores = sklearn.cross_validation.cross_val_score(clf, X, y, cv=5, n_jobs=4)
print scores
