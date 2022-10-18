import tensorflow
import tflearn
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize as tokenizer
import numpy
import random
import json
import pickle
from os import path

stemmer = LancasterStemmer()

data_path = "data/train"
data_name = "train"

with open("intent.json") as file:
    data = json.load(file)

try:
    with open(f"{data_path}/{data_name}.pickle", "rb") as file:
        words, labels, training, output = pickle.load(file)
except:
    words = []
    labels = []
    docs = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for text in intent["text"]:
            wrds = tokenizer(text)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
            
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    output_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        
        wrds = [stemmer.stem(w) for w in doc]
        
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
                
        output_row = output_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    
    with open(f"{data_path}/{data_name}.pickle", "wb") as file:
        pickle.dump((words, labels, training, output), file)

    #tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

if path.exists(f"{data_path}/{data_name}.tf.index") and path.exists(f"{data_path}/{data_name}.tf.meta"):
    model.load(f"{data_path}/{data_name}.tf")
else:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save(f"{data_path}/{data_name}.tf")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    
    s_words = tokenizer(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    for se in s_words:
        for i, w in enumerate(words):
          if w == se:
              bag[i] = 1
              
    return numpy.array(bag)

def chat():
    print("Talking")
    while True:
        inp = input("message:")
        if inp.lower() == "quit": break
        
        result = model.predict([bag_of_words(inp, words)])
        result_index = numpy.argmax(result)
        tag = labels[result_index]
        print(tag)
        
chat()