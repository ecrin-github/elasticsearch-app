import json
from configs import ES_MDR_RECORD_INDEX_NAME

from elasticsearch import Elasticsearch

elasticsearch_host = 'http://localhost:9200/'

es_client = Elasticsearch([elasticsearch_host], verify_certs=True)

# JSON file with mdr record index description
with open('./indices/mdr_record.json') as mdr_record_idx:
    mdr_record_index = json.load(mdr_record_idx)

# Creation of both indices
res_mdr_record = es_client.indices.create(index=ES_MDR_RECORD_INDEX_NAME, body=mdr_record_index, ignore=400)

if res_mdr_record:
    print('MDR Record index has been created!')
    print('==================================')
    print(res_mdr_record)
else:
    print(res_mdr_record)

