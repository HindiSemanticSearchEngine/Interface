# coding=utf-8
import os
from elasticsearch import Elasticsearch
from json import dumps
from SecretGoogleTranslationAPI import Translate

translation = Translate()

es = Elasticsearch("https://search-hsse-lw7qjjebuhv3pspk2v5jbtsfbq.us-west-2.es.amazonaws.com/")

##################################################################################################################################

from flask import Flask
from flask import request
from flask import render_template, redirect, url_for

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        query = request.form['text']

        return redirect(url_for('search', query = query))

##################################################################################################
@app.route('/heritage',methods = ['GET','POST'])
def heritage():
    if request.method == 'GET':
        return render_template("wikiHOME.html")
    else:
        query = request.form['text']

        return redirect(url_for('wiki', query = query))

@app.route('/search/heritage/?=<query>', methods = ['GET', 'POST'])
def wiki(query):
    if request.method == 'GET':

        searchDoc = {
            "size": 18,
            "query": {
                "dis_max": {
                    "queries": [
                        {
                            "match": {
                                "title": {
                                    "query": query,
                                    "boost": 2
                                }
                            }
                        },
                        {
                            "match": {
                                "description": {
                                    "query": query,
                                    "boost": 1.2
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [
                { "_score": { "order": "desc" }}
            ]
        }

        results = es.search(index = "heritage", doc_type = "doc", body = dumps(searchDoc))

        hindi_results = results

        for i,j in zip(results['hits']['hits'], hindi_results['hits']['hits']):
            title = i['_source']['title']
            description = i['_source']['description']
            j['_source']['description'] = translation.translate(description)
            j['_source']['title'] = translation.translate(title)
            print j['_source']['title']

        return render_template('wiki_results.html', results = hindi_results, search_text = query)
    else:
        return "Some Error Occured!"
##################################################################################################

@app.route('/search/news/?=<query>', methods = ['GET', 'POST'])
def search(query):
    if request.method == 'GET':

        searchDoc = {
            "size": 18,
            "query": {
                "dis_max": {
                    "queries": [
                        {
                            "match": {
                                "title": {
                                    "query": query,
                                    "boost": 2
                                }
                            }
                        },
                        {
                            "match": {
                                "description": {
                                    "query": query,
                                    "boost": 1.2
                                }
                            }
                        },
                        {
                            "match": {
                                "keywords": {
                                    "query": query,
                                    "boost": 1.5
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [
                { "_score": { "order": "desc" }},
                { "date":   { "order": "desc" }}
            ]
        }

        results = es.search(index = "hsse", doc_type = "doc", body = dumps(searchDoc))
        return render_template('search_results.html', results = results, search_text = query)
    else:
        return "Some Error Occured!"

if __name__ == '__main__':
    app.secret_key = 'hsse key'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug = True)
