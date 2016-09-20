# Shopping

## Prerequisite

### Django
This demo uses the Django web framework. It can be installed simply with `pip install django` command.

### Elasticsearch
This demo uses the Elasticsearch as the searching engine for data queries. To install Elasticsearch, one can simply run
`curl -L -O https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.0/elasticsearch-2.4.0.tar.gz`
command, and then extract the files with `tar -xf elasticsearch-2.4.-.tar.gz` command.
### Dependent python packages
- elasticsearch\_dsl
- elasticsearch


## Index data entries
In this demo, I use the electronic product dataset in
[SamTube405/Amazon-E-commerce-Data-set](https://github.com/SamTube405/Amazon-E-commerce-Data-set). To index the entries
into Elasticsearch, one can run the script in dataindexer, which will kill previous elasticsearch instance and then
parse the file within the same directory and index the entries into elasticsearch.

## Run the demo
After the data got indexed in elasticsearch, we can start the django server by running `python manage.py runserver`
command, and then we can check the demo by entering `http://127.0.0.1:8000/shop` into the address bar of any browser on
your choice.
