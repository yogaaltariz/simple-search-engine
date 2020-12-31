import re
import json
import pickle
import math
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from os import listdir


# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Clean string function
def preprocessing_doc(text) :  
    link = re.findall(r"<link>(.*?)</link>", lines[0])[0]
    title = re.findall(r"<title>(.*?)</title>", lines[1])[0]
    body = ''.join(lines[2:])  

    body = (body.encode('ascii', 'ignore')).decode("utf-8")
    body = re.sub("&.*?;", "", body)
    body = re.sub(">", "", body)    
    body = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", body)
    body = re.sub("-", " ", body)
    # body = re.sub(r'(?<=[.?!])( +|\Z)', r'\n', body)
    body = body.replace('.', '\n')
    body = re.sub("^\s+","" ,body)
    body = body.replace('\n', ' ').replace('\r', '').replace('  ',' ')
    body = body.lower()
    body = ' '.join(re.split('\.\s+',body))
    body = body.replace("http://", " ").replace("https://", " ")
    return link, title, body

CORPUS_PATH = './corpus/'
files = [CORPUS_PATH+f for f in listdir(CORPUS_PATH)]
stopwords = open('./stopwords.txt').read().split('\n')

df_data={}
tf_data={}
idf_data={}

i = 0
for file in files:
    tf={} 
    with open(file,'r') as data:
        lines = data.readlines()
        link, title, body = preprocessing_doc(lines)
        stemmed_body = stemmer.stem(body)
        for word in stemmed_body.split():
            if word in stopwords:
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
            'tf': tf,
            'caption': body[:255]
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
			'score' : weight,
            'caption': tf_data[data]['caption']
		}

        if doc['score'] != 0 :
            if doc not in list_doc:
                list_doc.append(doc)

    tf_idf[word] = list_doc


# Write dictionary to file
with open('./index/inverted_index.pickle', 'wb') as file:
     pickle.dump(tf_idf, file)