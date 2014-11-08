__author__ = 'andrewa'
#-*- coding: utf-8 -*-
import numpy as np
A = open('russian_words.txt', 'r').read().split('\n')
B = []
for i in A:
    i = i.split("|")
    B.append(i[3].strip())
C = open('russian_words_final.txt', 'w')
for i in B:
    C.write(i+'\n')
C.close()