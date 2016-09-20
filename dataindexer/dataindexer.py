from elasticsearch_dsl import String, DocType, Index
from elasticsearch import Elasticsearch
import io
import time
from subprocess import call

Product = None
es = None


def start_elastic_search():
    global es
    call('pkill -9 -f elasticsearch'.split())
    call('elasticsearch -d'.split())
    time.sleep(10)
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])


def get_field_list(file):
    return set([x.split('=')[0] for x in open(file).readlines() if '=' in x])


def create_product_class(file):
    global Product, es
    attrs = {field: String(multi=(True if field == 'Feature' else False))
             for field in get_field_list(file)}
    Product = type('Product', (DocType, ), attrs)
    i = Index('index', using=es)
    i.doc_type = Product
    i.delete(ignore=404)
    i.create()


def index_amazon_product_list(file):
    create_product_class(file)
    with io.open(file, encoding='utf8', errors='ignore') as f:
        features = []
        entry = dict()
        for line in f.readlines():
            if line[:3] == 'ITEM':
                continue
            if '=' not in line:
                entry['Feature'] = features
                product = Product(**entry)
                product.meta.index = 'index'
                product.save(using=es)
                features = []
                entry = dict()
                continue
            if line.split('=')[0] == 'Feature':
                features.append(line.split('=')[1])
            entry[line.split('=')[0]] = line.split('=')[1]


def main():
    start_elastic_search()
    index_amazon_product_list('./amazon_electronics.txt')

if __name__ == '__main__':
    main()
