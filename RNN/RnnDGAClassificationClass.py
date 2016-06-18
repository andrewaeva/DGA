import numpy as np
import pandas as pd
import theano
import theano.tensor as T
import lasagne

dataset = pd.read_csv('dataset_all.csv', sep = ',')
dataset.head()

chars = dataset['domain'].tolist()
chars = ''.join(chars)
chars = list(set(chars))

classes = dataset['class'].tolist()
classes = list(set(classes))

# Translating
char_to_ix = { ch:i for i,ch in enumerate(chars) }
ix_to_char = { i:ch for i,ch in enumerate(chars) }
class_to_y = { cl:i for i,cl in enumerate(classes) }

NUM_VOCAB = len(chars)
NUM_CLASS = len(classes)
NUM_CHARS = 75

N = len(dataset.index)
X = np.zeros((N, NUM_CHARS)).astype('int32')
M = np.zeros((N, NUM_CHARS)).astype('float32')
Y = np.zeros(N).astype('int32')

for i, r in dataset.iterrows():
    inputs = [char_to_ix[ch] for ch in r['domain']]
    length = len(inputs)
    X[i,:length] = np.array(inputs)
    M[i,:length] = np.ones(length)
    Y[i] = class_to_y[r['class']]

#Splitting for train and test sets
rand_indx = np.random.randint(N, size=N)
X = X[rand_indx,:]
M = M[rand_indx,:]
Y = Y[rand_indx]

Ntrain = int(N * 0.75)
Ntest = N - Ntrain

Xtrain = X[:Ntrain,:]
Mtrain = M[:Ntrain,:]
Ytrain = Y[:Ntrain]

Xtest = X[Ntrain:,:]
Mtest = M[Ntrain:,:]
Ytest = Y[Ntrain:]
#==============
#
#
# Model 1, simple GRU, and softmax as last classification layer
#
#
#==============
BATCH_SIZE = 100
NUM_UNITS_ENC = 128

x_sym = T.imatrix()
y_sym = T.ivector()
xmask_sym = T.matrix()

Tdata = np.random.randint(0,10,size=(BATCH_SIZE, NUM_CHARS)).astype('int32')
Tmask = np.ones((BATCH_SIZE, NUM_CHARS)).astype('float32')

l_in = lasagne.layers.InputLayer((None, None))
l_emb = lasagne.layers.EmbeddingLayer(l_in, NUM_VOCAB, NUM_VOCAB, name='Embedding')

print l_emb.name, lasagne.layers.get_output(l_emb, inputs={l_in: x_sym}).eval({x_sym: Tdata}).shape

l_mask_enc = lasagne.layers.InputLayer((None, None))

l_enc = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc)

print l_enc.name, lasagne.layers.get_output(l_enc, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape


l_last_hid = lasagne.layers.SliceLayer(l_enc, indices=-1, axis=1, name='LastState')

print l_last_hid.name, lasagne.layers.get_output(l_last_hid, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape

l_softmax = lasagne.layers.DenseLayer(l_last_hid, num_units=NUM_CLASS,
                                      nonlinearity=lasagne.nonlinearities.softmax,
                                      name='SoftmaxOutput')

print l_softmax.name, lasagne.layers.get_output(l_softmax, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape
print lasagne.layers.count_params(l_softmax)

output_train = lasagne.layers.get_output(l_softmax, inputs={l_in: x_sym, l_mask_enc: xmask_sym}, deterministic=False)

#cost function
total_cost = T.nnet.categorical_crossentropy(output_train, y_sym.flatten())
mean_cost = T.mean(total_cost)

#accuracy function
argmax = T.argmax(output_train, axis=-1)
eq = T.eq(argmax,y_sym)
acc = T.mean(eq)

all_parameters = lasagne.layers.get_all_params([l_softmax], trainable=True)

print "Trainable Model Parameters"
print "-"*40
for param in all_parameters:
    print param, param.get_value().shape
print "-"*40

all_grads = T.grad(mean_cost, all_parameters)
all_grads_clip = [T.clip(g,-1,1) for g in all_grads]
all_grads_norm = lasagne.updates.total_norm_constraint(all_grads_clip, 1)

updates = lasagne.updates.adam(all_grads_norm, all_parameters, learning_rate=0.005)
train_func_a = theano.function([x_sym, y_sym, xmask_sym], mean_cost, updates=updates)
test_func_a = theano.function([x_sym, y_sym, xmask_sym], acc)
#==============
#
#
#Model 2, Biderection GRU
#
#
#==============
BATCH_SIZE = 100
NUM_UNITS_ENC = 128

x_sym = T.imatrix()
y_sym = T.ivector()
xmask_sym = T.matrix()

Tdata = np.random.randint(0,10,size=(BATCH_SIZE, NUM_CHARS)).astype('int32')
Tmask = np.ones((BATCH_SIZE, NUM_CHARS)).astype('float32')

l_in = lasagne.layers.InputLayer((None, None))
l_emb = lasagne.layers.EmbeddingLayer(l_in, NUM_VOCAB, NUM_VOCAB, name='Embedding')

print l_emb.name, lasagne.layers.get_output(l_emb, inputs={l_in: x_sym}).eval({x_sym: Tdata}).shape

l_mask_enc = lasagne.layers.InputLayer((None, None))

#BIDERECTION
l_enc_fwd = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc, backwards=False)
l_enc_bwd = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc, backwards=True)
l_enc = lasagne.layers.ConcatLayer([l_enc_fwd, l_enc_bwd], axis=2)

#l_enc = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc)

print l_enc.name, lasagne.layers.get_output(l_enc, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape


l_last_hid = lasagne.layers.SliceLayer(l_enc, indices=-1, axis=1, name='LastState')

print l_last_hid.name, lasagne.layers.get_output(l_last_hid, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape

l_softmax = lasagne.layers.DenseLayer(l_last_hid, num_units=NUM_CLASS,
                                      nonlinearity=lasagne.nonlinearities.softmax,
                                      name='SoftmaxOutput')

print l_softmax.name, lasagne.layers.get_output(l_softmax, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape
print lasagne.layers.count_params(l_softmax)


output_train = lasagne.layers.get_output(l_softmax, inputs={l_in: x_sym, l_mask_enc: xmask_sym}, deterministic=False)

#cost function
total_cost = T.nnet.categorical_crossentropy(output_train, y_sym.flatten())
mean_cost = T.mean(total_cost)

#accuracy function
argmax = T.argmax(output_train, axis=-1)
eq = T.eq(argmax,y_sym)
acc = T.mean(eq)

all_parameters = lasagne.layers.get_all_params([l_softmax], trainable=True)

print "Trainable Model Parameters"
print "-"*40
for param in all_parameters:
    print param, param.get_value().shape
print "-"*40

all_grads = T.grad(mean_cost, all_parameters)
all_grads_clip = [T.clip(g,-1,1) for g in all_grads]
all_grads_norm = lasagne.updates.total_norm_constraint(all_grads_clip, 1)

updates = lasagne.updates.adam(all_grads_norm, all_parameters, learning_rate=0.005)
train_func_b = theano.function([x_sym, y_sym, xmask_sym], mean_cost, updates=updates)
test_func_b = theano.function([x_sym, y_sym, xmask_sym], acc)
#==============
#
#
# Model 3, Biderection GRU and Attention
#
#
#==============
from decoder_attention import LSTMAttentionDecodeLayer

BATCH_SIZE = 100
NUM_UNITS_ENC = 128
MAX_DIGITS = 75

x_sym = T.imatrix()
y_sym = T.ivector()
xmask_sym = T.matrix()

Tdata = np.random.randint(0,10,size=(BATCH_SIZE, NUM_CHARS)).astype('int32')
Tmask = np.ones((BATCH_SIZE, NUM_CHARS)).astype('float32')

l_in = lasagne.layers.InputLayer((None, None))
l_emb = lasagne.layers.EmbeddingLayer(l_in, NUM_VOCAB, NUM_VOCAB, name='Embedding')

print l_emb.name, lasagne.layers.get_output(l_emb, inputs={l_in: x_sym}).eval({x_sym: Tdata}).shape

l_mask_enc = lasagne.layers.InputLayer((None, None))

#BIDERECTION
l_enc_fwd = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc, backwards=False)
l_enc_bwd = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc, backwards=True)
l_enc = lasagne.layers.ConcatLayer([l_enc_fwd, l_enc_bwd], axis=2)

#l_enc = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc)

print l_enc.name, lasagne.layers.get_output(l_enc, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape

l_dec = LSTMAttentionDecodeLayer(l_enc,
                                        num_units=NUM_UNITS_ENC,
                                        aln_num_units=NUM_UNITS_ENC,
                                        n_decodesteps=1,
                                        name='LSTMDecoder')

#l_reshape = lasagne.layers.ReshapeLayer(l_dec, (-1, [1]))

print "LSTMAttentionDecodeLayer ", lasagne.layers.get_output(l_dec, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape

l_softmax = lasagne.layers.DenseLayer(l_dec, num_units=NUM_CLASS,
                                      nonlinearity=lasagne.nonlinearities.softmax,
                                      name='SoftmaxOutput')

#l_out = lasagne.layers.ReshapeLayer(l_softmax, (x_sym.shape[0], -1, NUM_CLASS))
print lasagne.layers.get_output(l_softmax, inputs={l_in: x_sym, l_mask_enc: xmask_sym}, deterministic=False).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape
print lasagne.layers.count_params(l_softmax)


output_train = lasagne.layers.get_output(l_softmax, inputs={l_in: x_sym, l_mask_enc: xmask_sym}, deterministic=False)

#cost function
total_cost = T.nnet.categorical_crossentropy(output_train, y_sym.flatten())
mean_cost = T.mean(total_cost)

#accuracy function
argmax = T.argmax(output_train, axis=-1)
eq = T.eq(argmax,y_sym)
acc = T.mean(eq)

all_parameters = lasagne.layers.get_all_params([l_softmax], trainable=True)

print "Trainable Model Parameters"
print "-"*40
for param in all_parameters:
    print param, param.get_value().shape
print "-"*40

all_grads = T.grad(mean_cost, all_parameters)
all_grads_clip = [T.clip(g,-1,1) for g in all_grads]
all_grads_norm = lasagne.updates.total_norm_constraint(all_grads_clip, 1)

updates = lasagne.updates.adam(all_grads_norm, all_parameters, learning_rate=0.005)
train_func_c = theano.function([x_sym, y_sym, xmask_sym], mean_cost, updates=updates)
test_func_c = theano.function([x_sym, y_sym, xmask_sym], acc)
#==============
#
#
# Model 4, Biderection GRU + Two Attention
#
#
#==============
from decoder_attention import LSTMAttentionDecodeLayer

BATCH_SIZE = 100
NUM_UNITS_ENC = 128
MAX_DIGITS = 75

x_sym = T.imatrix()
y_sym = T.ivector()
xmask_sym = T.matrix()

Tdata = np.random.randint(0,10,size=(BATCH_SIZE, NUM_CHARS)).astype('int32')
Tmask = np.ones((BATCH_SIZE, NUM_CHARS)).astype('float32')

l_in = lasagne.layers.InputLayer((None, None))
l_emb = lasagne.layers.EmbeddingLayer(l_in, NUM_VOCAB, NUM_VOCAB, name='Embedding')

print l_emb.name, lasagne.layers.get_output(l_emb, inputs={l_in: x_sym}).eval({x_sym: Tdata}).shape

l_mask_enc = lasagne.layers.InputLayer((None, None))

#BIDERECTION
l_enc_fwd = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc, backwards=False)


#l_enc = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc)

print l_enc_fwd, lasagne.layers.get_output(l_enc_fwd, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape

l_dec_fwd = LSTMAttentionDecodeLayer(l_enc_fwd,
                                        num_units=NUM_UNITS_ENC,
                                        aln_num_units=NUM_UNITS_ENC,
                                        n_decodesteps=1,
                                        name='LSTMDecoder')

print "LSTMAttentionDecodeLayer ", lasagne.layers.get_output(l_dec_fwd, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape

l_enc_bwd = lasagne.layers.GRULayer(l_emb, num_units=NUM_UNITS_ENC, name='GRUEncoder', mask_input=l_mask_enc, backwards=True)

print l_enc_bwd, lasagne.layers.get_output(l_enc_bwd, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape

l_dec_bwd = LSTMAttentionDecodeLayer(l_enc_bwd,
                                        num_units=NUM_UNITS_ENC,
                                        aln_num_units=NUM_UNITS_ENC,
                                        n_decodesteps=1,
                                        name='LSTMDecoder')

print "LSTMAttentionDecodeLayer ", lasagne.layers.get_output(l_dec_bwd, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape


l_dec = lasagne.layers.ConcatLayer([l_dec_fwd, l_dec_bwd], axis=2)

print l_dec, lasagne.layers.get_output(l_dec, inputs={l_in: x_sym, l_mask_enc: xmask_sym}).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape

l_softmax = lasagne.layers.DenseLayer(l_dec, num_units=NUM_CLASS,
                                      nonlinearity=lasagne.nonlinearities.softmax,
                                      name='SoftmaxOutput')

#l_out = lasagne.layers.ReshapeLayer(l_softmax, (x_sym.shape[0], -1, NUM_CLASS))
print lasagne.layers.get_output(l_softmax, inputs={l_in: x_sym, l_mask_enc: xmask_sym}, deterministic=False).eval(
    {x_sym: Tdata, xmask_sym: Tmask}).shape
print lasagne.layers.count_params(l_softmax)


output_train = lasagne.layers.get_output(l_softmax, inputs={l_in: x_sym, l_mask_enc: xmask_sym}, deterministic=False)

#cost function
total_cost = T.nnet.categorical_crossentropy(output_train, y_sym.flatten())
mean_cost = T.mean(total_cost)

#accuracy function
argmax = T.argmax(output_train, axis=-1)
eq = T.eq(argmax,y_sym)
acc = T.mean(eq)

all_parameters = lasagne.layers.get_all_params([l_softmax], trainable=True)

print "Trainable Model Parameters"
print "-"*40
for param in all_parameters:
    print param, param.get_value().shape
print "-"*40

all_grads = T.grad(mean_cost, all_parameters)
all_grads_clip = [T.clip(g,-1,1) for g in all_grads]
all_grads_norm = lasagne.updates.total_norm_constraint(all_grads_clip, 1)

updates = lasagne.updates.adam(all_grads_norm, all_parameters, learning_rate=0.005)
train_func_d = theano.function([x_sym, y_sym, xmask_sym], mean_cost, updates=updates)
test_func_d = theano.function([x_sym, y_sym, xmask_sym], acc)


Xbatch = Xtrain[:BATCH_SIZE,:]
Mbatch = Mtrain[:BATCH_SIZE,:]
Ybatch = Ytrain[:BATCH_SIZE]

train_func_a(Xbatch, Ybatch, Mbatch)
train_func_b(Xbatch, Ybatch, Mbatch)
train_func_c(Xbatch, Ybatch, Mbatch)
train_func_d(Xbatch, Ybatch, Mbatch)

def test_acc_a():
    acc = 0
    b = 0
    n = 0
    while b < Ntest:
        Xbatch = Xtest[b:b+BATCH_SIZE,:]
        Mbatch = Mtest[b:b+BATCH_SIZE,:]
        Ybatch = Ytest[b:b+BATCH_SIZE]
        acc += test_func_a(Xbatch, Ybatch, Mbatch)
        b += BATCH_SIZE
        n += 1
    return acc / n

def test_acc_b():
    acc = 0
    b = 0
    n = 0
    while b < Ntest:
        Xbatch = Xtest[b:b+BATCH_SIZE,:]
        Mbatch = Mtest[b:b+BATCH_SIZE,:]
        Ybatch = Ytest[b:b+BATCH_SIZE]
        acc += test_func_b(Xbatch, Ybatch, Mbatch)
        b += BATCH_SIZE
        n += 1
    return acc / n

def test_acc_c():
    acc = 0
    b = 0
    n = 0
    while b < Ntest:
        Xbatch = Xtest[b:b+BATCH_SIZE,:]
        Mbatch = Mtest[b:b+BATCH_SIZE,:]
        Ybatch = Ytest[b:b+BATCH_SIZE]
        acc += test_func_c(Xbatch, Ybatch, Mbatch)
        b += BATCH_SIZE
        n += 1
    return acc / n

def test_acc_d():
    acc = 0
    b = 0
    n = 0
    while b < Ntest:
        Xbatch = Xtest[b:b+BATCH_SIZE,:]
        Mbatch = Mtest[b:b+BATCH_SIZE,:]
        Ybatch = Ytest[b:b+BATCH_SIZE]
        acc += test_func_d(Xbatch, Ybatch, Mbatch)
        b += BATCH_SIZE
        n += 1
    return acc / n

# -*- coding: utf-8 -*-
import matplotlib as mpl
mpl.rcdefaults() # Reset by default
mpl.rcParams['font.family'] = 'fantasy'
mpl.rcParams['font.fantasy'] = 'Ubuntu'

import matplotlib.pyplot as plt
from IPython import display
%matplotlib inline
%matplotlib nbagg

val_interval = BATCH_SIZE * 10
samples_processed = 0
val_samples = []

accs_a, accs_b, accs_c, accs_d = [], [], [], []

flag = True
plt.figure()

for e in range(10):
    rand_indx = np.random.randint(Ntrain, size=Ntrain)
    Xtrain = Xtrain[rand_indx,:]
    Mtrain = Mtrain[rand_indx,:]
    Ytrain = Ytrain[rand_indx]
    b = 0
    while b < Ntrain:
        Xbatch = Xtrain[b:b+BATCH_SIZE,:]
        Mbatch = Mtrain[b:b+BATCH_SIZE,:]
        Ybatch = Ytrain[b:b+BATCH_SIZE]

        #Training Models
        train_func_a(Xbatch, Ybatch, Mbatch) #GRU
        train_func_b(Xbatch, Ybatch, Mbatch) #Biderection
        train_func_c(Xbatch, Ybatch, Mbatch) #Concat (two GRU) + Attention
        train_func_d(Xbatch, Ybatch, Mbatch) #Concat(GRU + Attention)

        b += BATCH_SIZE

        samples_processed += BATCH_SIZE

        if samples_processed % val_interval == 0:

            val_samples += [samples_processed]

            accs_a += [test_acc_a()]
            accs_b += [test_acc_b()]
            accs_c += [test_acc_c()]
            accs_d += [test_acc_d()]

            plt.plot(val_samples, accs_a, 'r', label = u'Model 1')
            plt.plot(val_samples, accs_b, 'g', label = u'Model 2')
            plt.plot(val_samples, accs_c, 'b', label = u'Model 3')
            plt.plot(val_samples, accs_d, 'y', label = u'Model 4')

            if flag == True:
                plt.legend(loc='lower right')
                flag = False

            plt.ylabel(u'Validation Accuracy', fontsize=15)
            plt.xlabel(u'Processed samples', fontsize=15)
            plt.title('', fontsize=20)
            plt.grid('on')
            display.display(plt.gcf())
            display.clear_output(wait=True)
            plt.show()
