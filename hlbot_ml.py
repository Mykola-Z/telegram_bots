# -*- coding: utf-8 -*-
"""
Created on Mon May 4 11:44:45 2020

@author: mzly903
"""
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import glob
import random

files = glob.glob(r'C:/Users/mzly903/Desktop/PhD/1. Code/Python/telegram_bot/hl/base/m*')
all_messa = []
for file in files:
    text_in = open(file, 'r',  encoding='utf8')
    list_messages = list(text_in.read().split('<div class="text">\n'))
    for u in range(len(list_messages)):
        crop = list_messages[u].find('       </div>')
        list_messages[u] = list_messages[u][:crop]
    all_messa.append(list_messages[2:])

merged_list = []

for l in all_messa:
    merged_list += l
better_list = []
for single_message in merged_list:
    if single_message[-1:] == "?":
        single_message = single_message[:-1]
    single_message = single_message.lower()
    current = list(single_message.split(' '))
    better_list.append(current)

# text = "серый привет"
# words_in_text = text.split(' ')
# indices = [i for i, s in enumerate(better_list) if [i for i in words_in_text if i in s]]
# print(better_list[indices[28]])

words = []
labls = []
docs_x = []
docs_y = []

for i in range(len(indices)):
    pattern = merged_list[indices[i]]
    wrds = ntkl.word_tokenize(pattern)
    words.extend(wrds)
    docs_x.append(wrds)
    docs_y.append(merged_list[indices[i]])
    

if merged_list[indices[i]] not in labels:
    labels.append(merged_list[indices[i]])


words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
output = numpy.array(output)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def chat_message(inp):

    results = model.predict([bag_of_words(inp, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    responses = []
    for tg in lables:
        if tg in tag:
            responses.append(tg)

    return random.choice(responses)
