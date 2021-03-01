import requests
from configs import ELASTICSEARCH_HOST


def get_indices():
    res = requests.get('{}/_cat/indices'.format(ELASTICSEARCH_HOST))
    print(res.text)
    return res


get_indices()
