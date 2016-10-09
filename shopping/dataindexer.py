import urllib2
import json
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk, bulk
import os
from functools import partial
from subprocess import call
import subprocess


api_key = 'xxjy9c67qp4mrfkufqtc5xvx'
page_size = 10
data_keyword = 'laptop'


def get_walmart_data(num):
    query = 'http://api.walmartlabs.com/v1/search?apiKey='+api_key+'&query='+data_keyword
    data = json.load(urllib2.urlopen(query))
    num = min(num, data['totalResults'])
    n_page = num / page_size
    fields = data['items'][-1].keys()
    ret = []
    counter = 0
    for i in range(n_page):
        counter += 1
        if counter == 5:
            time.sleep(1)
            counter = 0
        query = 'http://api.walmartlabs.com/v1/search?apiKey='+api_key+'&query='+data_keyword+'&start='+str(page_size*i+1)
        ret += json.load(urllib2.urlopen(query))['items']
    return ret


def elastic_search_running():
    ps = subprocess.Popen('ps aux'.split(), stdout=subprocess.PIPE)
    output = subprocess.check_output('grep elastic'.split(), stdin=ps.stdout)

    return 'java' in output


def start_elastic_search():
    if elastic_search_running():
        print 'Elastic Search is already running!'
        return True
    call('pkill -9 -f elasticsearch'.split())
    call('./elasticsearch/bin/elasticsearch -d'.split())
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
    counter = 0
    while not es.ping():
        time.sleep(1)
        if counter > 10:
            return False
    return True


def index_data(es, data):
    data = map(lambda x: {'_op_type': 'create', '_index': 'walmart', '_type': 'document', '_source': x}, data)
    res = bulk(es, data)
    print res


def get_data_ready():
    if not start_elastic_search():
        return
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
    if not es.indices.exists('walmart'):
        es.indices.create(index='walmart', body={'settings': {'number_of_shards': 1, 'number_of_replicas': 0}})
    if es.search(index='walmart', body={'query': {'match_all': {}}})['hits']['total'] < 100:
        data = get_walmart_data(500)
        index_data(es, data)
    print 'data is ready!'
