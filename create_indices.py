import json

from elasticsearch import Elasticsearch

elasticsearch_host = 'http://localhost:9200/'

es_client = Elasticsearch([elasticsearch_host], verify_certs=True)

# JSON file with study index description
with open('./indices/study.json') as study_indices:
    study_index = json.load(study_indices)

# JSON file with data object index description
with open('./indices/data_object.json') as data_object_indices:
    data_object_index = json.load(data_object_indices)

# Creation of both indices
res_study = es_client.indices.create(index='study', body=study_index, ignore=400)
res_do = es_client.indices.create(index='data-object', body=data_object_index, ignore=400)

if res_study:
    # print('Study index was created!')
    print(res_study)
else:
    print(res_study)

if res_do:
    # print('Data object index was created!')
    print(res_do)
else:
    print(res_do)

