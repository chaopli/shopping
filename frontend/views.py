from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
page_size = 9



def index(request):
    init_page = 1
    return get_objects(request, page=init_page)


def get_all_objs():
    s = Search(using=es).query('match_all').query(Q('bool', must=[Q('exists', field='Title')])).fields(['Title', 'ListPrice'])
    return s


def filter_on_brand(s, brand):
    return s.query(Q('bool', must=[Q('match', Brand=brand)])) if brand else s


def query_on_page(s, page):
    page = 1 if not page else page
    start, end = (page-1)*page_size, (page-1)*page_size+page_size
    return s[start:end]


def create_search_object(page, brand):
    s = get_all_objs()
    s = filter_on_brand(s, brand)
    s = query_on_page(s, page)
    return s


query_combinators = [filter_on_brand, query_on_page]


def get_objects(request, *args, **kwargs):
    print args
    print kwargs
    print request.get_full_path()
    page = 1 if not request.GET.get('page') else int(request.GET.get('page'))
    brand = request.GET.get('brand')
    print page
    print brand, type(brand)
    s = create_search_object(page, brand)
    result = [r.to_dict() for r in s.execute().hits]
    return get_render_result(request, result, get_all_brands(), page, s.count()/page_size, brand)


def get_render_result(request, objects, brands, cur_page, n_page, cur_brand):
    return render(request, 'frontend/index.html', {'objects': objects,
                                                   'n_page': n_page,
                                                   'brands': brands,
                                                   'cur_brand': cur_brand,
                                                   'pages': {'1': cur_page, '2': cur_page+1, '3': cur_page+2}})


def get_all_brands():
    s = Search(using=es).query('match_all').query(Q('bool', must=[Q('exists', field='Brand')]))
    brands = set([r.to_dict()['Brand'] for r in s.execute().hits])
    return brands

