from typing import Optional
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles

import pickle
import sys
import json

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/site", StaticFiles(directory="site", html = True), name="site")

async def find_results(queries):
    with open('../index/inverted_index.pickle', 'rb') as indexdb:
        results = []
        indexFile = pickle.load(indexdb)
        #query
        list_doc = {}

        for q in queries.split():
            q = stemmer.stem(q)
            try :
                for doc in indexFile[q]:
                    if doc['url'] in list_doc :
                        list_doc[doc['url']]['score'] += doc['score']
                    else :
                        list_doc[doc['url']] = doc
            except :
                continue

        #convert to list
        list_data=[]
        for data in list_doc :
            list_data.append(list_doc[data])

            #sorting list descending
        count=1;
        for data in sorted(list_data, key=lambda k: k['score'], reverse=True):
            json_str = json.dumps(data)
            json_parse = json.loads(json_str)
            results.append(json_parse)

        return results


@app.get("/api")
async def read_root(search: Optional[str] = Query(None, max_length=50)):
    results = await find_results(search)
    return {"results": results}
