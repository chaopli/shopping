# Shopping
[![Build Status](https://travis-ci.org/chaopli/shopping.svg?branch=master)](https://travis-ci.org/chaopli/shopping)
## Prerequisite

### Django
This demo uses the Django web framework. It can be installed simply with `pip install django` command.

### Elasticsearch
This demo uses the Elasticsearch as the searching engine for data queries. To install Elasticsearch, one can simply run
`curl -L -O https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.0/elasticsearch-2.4.0.tar.gz`
command, and then extract the files with `tar -xf elasticsearch-2.4.0.tar.gz` command.
### Dependent python packages
- elasticsearch\_dsl
- elasticsearch


## Index data entries
In this demo, I use the laptop data set from Walmart Lab ecommerce product api. This data will be fetched from Walmart Lab api if this 
project is started as the first time.

## Run the demo
After the data got indexed in elasticsearch, we can start the django server by running `python manage.py runserver`
command, and then we can check the demo by entering `http://127.0.0.1:8000/shop` into the address bar of any browser on
your choice.
