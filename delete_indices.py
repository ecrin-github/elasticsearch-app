import requests
from configs import ELASTICSEARCH_HOST, ES_OBJECT_INDEX_NAME, ES_STUDY_INDEX_NAME
from get_indices import get_indices


def delete_indices():
    study = requests.delete('{}/{}'.format(ELASTICSEARCH_HOST, ES_STUDY_INDEX_NAME))
    data_object = requests.delete('{}/{}'.format(ELASTICSEARCH_HOST, ES_OBJECT_INDEX_NAME))

    print(study.text)
    print(data_object.text)

    get_indices()


delete_indices()