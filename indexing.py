import re
import sys
import json
import pickle
import math
from os import listdir
import copy

# Clean string function
def clean_str(text) :    
    text = (text.encode('ascii', 'ignore')).decode("utf-8")
    text = re.sub("&.*?;", "", text)
    text = re.sub(">", "", text)    
    text = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", text)
    text = re.sub("-", " ", text)
    text = re.sub("\.+", "", text)
    text = re.sub("^\s+","" ,text)
    text = text.lower()
    return text

CORPUS_PATH = './corpus/'

files = [CORPUS_PATH+f for f in listdir(CORPUS_PATH)]

sw = open('./stopwords.txt').read().split('\n')


df_data={}
tf_data={}
idf_data={}

i = 0
for file in files:
    tf={} 
    with open(file, 'r') as data:
        lines = data.readlines()
        body = copy.copy(lines[2:])
        body = ''.join(body)
        text = ''.join(lines)
        title = re.findall(r"<title>(.*?)</title>", text)[0]
        link = re.findall(r"<link>(.*?)</link>", text)[0]
        # print(link)
        words = clean_str(body).split(' ')

        for word in words:
            word = word.replace('\n','')
            if word in sw:
                continue
            
            #tf term frequency
            if word in tf :
                tf[word] += 1
            else :
                tf[word] = 1

            #df document frequency
            if word in df_data :
                df_data[word] += 1
            else :
                df_data[word] = 1

        tf_data[link] = {
            'title': title,
            'tf': tf
        }

# Calculate Idf
for x in df_data :
   idf_data[x] = 1 + math.log10(len(tf_data)/df_data[x])


tf_idf = {}

for word in df_data:
    list_doc = []
    for data in tf_data: 
        tf_value = 0
        if word in tf_data[data]['tf']:
            tf_value = tf_data[data]['tf'][word]

        weight = tf_value * idf_data[word]
        # print(weight)
        doc = {
			'url' : data,
			'title' : tf_data[data]['title'],
			'score' : weight
		}

        if doc['score'] != 0 :
            if doc not in list_doc:
                list_doc.append(doc)

    tf_idf[word] = list_doc


# Write dictionary to file
with open('index.pickle', 'wb') as file:
     pickle.dump(tf_idf, file)