from six.moves.html_parser import HTMLParser
from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, A

es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
page_size = 9

def index(request):
    init_page = 1
    return get_objects(request, page=init_page)


def get_all_objs():
    s = Search(using=es, index='walmart').query('match_all').filter('exists', field='msrp').fields(['name',
                                                                                                    'msrp',
                                                                                                    'thumbnailImage',
                                                                                                    'shortDescription'])
    return s


def query_on_page(s, page):
    page = 1 if not page or page > s.count() / page_size else page
    start, end = (page-1)*page_size, (page-1)*page_size+page_size
    return s[start:end]


def filter_on_price(s, price):
    lo, hi = price.split('-')
    if lo != '*' and hi != '*':
        return s.filter('range', msrp={'gte': lo, 'lte': hi})
    elif lo != '*' and hi == '*':
        return s.filter('range', msrp={'gte': lo})
    elif lo == '*' and hi != '*':
        return s.filter('range', msrp={'lte': hi})
    else:
        return s


def search_on_keyword(s, sk):
    if not sk:
        return s
    else:
        return s.filter('term', longDescription=sk)


def create_search_object(page, price, sk):
    s = get_all_objs()
    s = filter_on_price(s, price)
    s = query_on_page(s, page)
    s = search_on_keyword(s, sk)
    return s


def get_objects(request, *args, **kwargs):
    print request.get_full_path()
    page = int(request.GET.get('page', '1'))
    price = request.GET.get('price', '*-*')
    sk = request.GET.get('search', '')
    s = create_search_object(page, price, sk)
    result = [r.to_dict() for r in s.execute().hits]
    return get_render_result(request, result, get_price_buckets(), page, s.count()/page_size, price, sk)


def get_render_result(request, objects, price_ranges, cur_page, n_page, cur_price, sk):
    return render(request, 'frontend/index.html', {'objects': [{'name': str(obj['name'][-1]),
                                                                'msrp': str(obj['msrp'][-1]),
                                                                'thumb': str(obj['thumbnailImage'][-1]),
                                                                'desc': HTMLParser().unescape(str(obj['shortDescription'][-1])) if 'shortDescription' in obj else ''} for obj in objects],
                                                   'n_page': n_page,
                                                   'price_ranges': price_ranges,
                                                   'pages': {'1': cur_page, '2': cur_page+1, '3': cur_page+2},
                                                   'cur_price': cur_price,
                                                   'sk': sk})


def get_price_buckets():
    a = A('range', field='msrp', ranges=[{'to': 100},
                                         {'from': 100, 'to': 200},
                                         {'from': 200, 'to': 300},
                                         {'from': 300, 'to': 400}])
    s = Search(using=es, index='walmart')
    s.aggs.bucket('price_ranges', a)
    res = s.execute()
    print res
    for x in res.aggregations.price_ranges.buckets:
        print x
    return [x['key'] for x in res.aggregations.price_ranges.buckets]

