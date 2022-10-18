import tensorflow
import tflearn
from nltk.stem.lancaster import LancasterStemmer
from nltk import word_tokenize as tokenizer
from nltk import download as nltk_download
import numpy
import random
import json
import pickle
from os import path

#Faz o download do pacote punkt caso não exista
nltk_download('punkt')

#define o stemmer
stemmer = LancasterStemmer()

#variaveis que definem o caminho e o nome dos arquivos
data_path = "data/train"
data_name = "train"

#abre o arquivo de falas e questões
with open("intent.json", encoding="UTF-8") as file:
    data = json.load(file)

#tenta carregar os dados de treino e variaveis de outros treinos no caminho selecionado
try:
    with open(f"{data_path}/{data_name}.pickle", "rb") as file:
        words, labels, training, output = pickle.load(file)
except:
    #
    words = []
    labels = []
    docs = []
    docs_x = []
    docs_y = []

    #cria a base de bag_of_words
    for intent in data["intents"]:
        for text in intent["text"]:
            wrds = tokenizer(text)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    #realiza a função de stam nas palavras para torna-las palavras base  //EX: criarei = criar, comerei = comer
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    #cria a saida do bag nula
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

    #cria o array usado para treinar a AI
    training = numpy.array(training)
    output = numpy.array(output)
    
    #cria o arquivo de treino da AI caso não exista
    with open(f"{data_path}/{data_name}.pickle", "wb") as file:
        pickle.dump((words, labels, training, output), file)

    #tensorflow.reset_default_graph()

#define a rede neural
net = tflearn.input_data(shape=[None, len(training[0])])
#conecta 16 neuronios a outros 16 onde cada um está conectado a autro
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 16)
#cria os neuronios de saída usando o padrão de softmax que tem uma saída baseado em % de certeza de cada neuronio
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

#tenta abrir os dados ja treinados caso não consiga, a IA ira ser treinada e salvará os dados
if path.exists(f"{data_path}/{data_name}.tf.index") and path.exists(f"{data_path}/{data_name}.tf.meta"):
    model.load(f"{data_path}/{data_name}.tf")
else:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save(f"{data_path}/{data_name}.tf")

#cria o bag_of_words final
def bag_of_words(s, words):
    #cria um bag nulo
    bag = [0 for _ in range(len(words))]
    
    #tokeniza as palavras
    s_words = tokenizer(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    #coloca 1 caso a palavra exista
    for se in s_words:
        for i, w in enumerate(words):
          if w == se:
              bag[i] = 1
              
    return numpy.array(bag)

def chat():
    print("Talking")
    while True:
        inp = input("Você:")
        if inp.lower() == "quit": break
        
        result = model.predict([bag_of_words(inp, words)])
        result_index = numpy.argmax(result)
        tag = labels[result_index]
        for i in data["intents"]:
            if i["tag"] == tag:
                tex = i["response"][random.randrange(0, len(i["response"]))]
                print(f"Lyra: {tex}")


def single_response(inp):
    #envia o texto para a AI
    result = model.predict([bag_of_words(inp, words)])
    #obtem o resultado em % e tranforma em nome de question TAG
    result_index = numpy.argmax(result)
    tag = labels[result_index]

    #procura a tag no arquivo e puxa um resposta dentro do arquivo
    for i in data["intents"]:
        if i["tag"] == tag:
            tex = i["response"][random.randrange(0, len(i["response"]))]
            return tex
        
#chat()
#print(single_response("ola tudo bem"))