import requests
from configs import ELASTICSEARCH_HOST, ES_MDR_RECORD_INDEX_NAME
from get_indices import get_indices


def delete_indices():
    mdr_record_index = requests.delete('{}/{}'.format(ELASTICSEARCH_HOST, ES_MDR_RECORD_INDEX_NAME))
    print(mdr_record_index.text)
    get_indices()


delete_indices()
