__author__ = 'andrewa'
#-*- coding: utf-8 -*-
import numpy as np
#A = open('russian_words.txt', 'r').read().split('\n')
#B = []
#for i in A:
#    i = i.split("|")
#    B.append(i[3].strip())
#C = open('russian_words_final.txt', 'w')
#for i in B:
#    C.write(i+'\n')
#C.close()

#alexa = open('../alexa.csv', 'r').read().split('\n')
#alexa_domain = []
#for i in alexa:
#    i = i.split(',')
#    try:
#        alexa_domain.append(i[1])
#    except:
#        pass
#opendns_random = open('opendns-random-domains.txt', 'r').read().split('\n')
#opendns_top = open('opendns-top-domains.txt', 'r').read().split('\n')
#opendns_random.extend(alexa_domain)
#opendns_random.extend(opendns_top)
#C = open('../all_legit.txt', 'w')
#C.seek(0)
#for i in opendns_random:
#    C.write(i+' 0\n')

######################################################
cryptolocker = open('cryptolocker.txt', 'r').read().split('\n')
zeus = open('zeus.txt', 'r').read().split('\n')
pushdo = open('pushdo.txt').read().split('\n')
others_dga = open('../dga_detection/dga_domains.txt', 'r').read().split('\n')
dds = open('dds-malicious-domains.csv', 'r').read().split('\n')
rovnix = open('rovnix.txt', 'r').read().split('\n')
tinba = open('tinba.txt', 'r').read().split('\n')
conficker = open('conficker.txt', 'r').read().split('\n')
matsnu = open('matsnu.txt', 'r').read().split('\n')
ramdo = open('ramdo.txt', 'r').read().split('\n')
goz = []
new_goz = []
goz_txt = open('goz.txt', 'w')
new_goz_txt = open('new_goz.txt', 'w')
for i in dds:
    i = i.split(',')
    if i[1] == '"cryptolocker"':
        cryptolocker.append(i[0].replace('"', ''))
    if i[1] == '"goz"':
        goz.append(i[0].replace('"', ''))
        goz_txt.write(i[0].replace('"', '')+'\n')
    if i[1] == '"newgoz"':
        new_goz.append(i[0].replace('"', ''))
        new_goz_txt.write(i[0].replace('"', '')+'\n')
C = open('../all_dga.txt', 'w')
C.seek(0)
for i in cryptolocker:
    C.write(i+' 1\n')
for i in zeus:
    C.write(i+' 2\n')
for i in pushdo:
    C.write(i+' 3\n')
for i in goz:
    C.write(i+' 4\n')
for i in new_goz:
    C.write(i+' 5\n')
for i in others_dga:
    C.write(i+' 6\n')
for i in rovnix:
    C.write(i+' 7\n')
for i in tinba:
    C.write(i+' 8\n')
for i in conficker:
    C.write(i.strip()+' 9\n')
for i in matsnu:
    C.write(i+' 10\n')
for i in ramdo:
    C.write(i+' 11\n')
C.close()