import os
from elasticsearch import Elasticsearch
from json import dumps

es = Elasticsearch("AWS Elasticsearch Cluster API URI")

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
                                    "boost": 1.5
                                }
                            }
                        },
                        {
                            "match": {
                                "keywords": {
                                    "query": query,
                                    "boost": 1.2
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

        results = es.search(index = "hsse", doc_type = "doc", body = dumps(searchDoc), sort = "_score")
        return render_template('search_results.html', results = results, search_text = query)
    else:
        return "Some Error Occured!"

if __name__ == '__main__':
    app.secret_key = 'Some Secret Key'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug = True)
