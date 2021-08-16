import os
import json
import requests

from elasticsearch import Elasticsearch
from configs import ELASTICSEARCH_HOST, ES_STUDY_INDEX_NAME, ES_OBJECT_INDEX_NAME

from converters import *


es_client = Elasticsearch([ELASTICSEARCH_HOST], verify_certs=True)


def add_studies(start_with):
    for indx in range(start_with, 8):
        # Path to studies folder
        directory = '/Users/iproger/sFTP/data/studies/studies{}/'.format(indx)
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                full_path = r'{}{}'.format(directory, filename)
                try:
                    with open(full_path, 'r') as opened_file:
                        json_data = json.load(opened_file)
                        study = study_converter(json_data)
                        headers = {'Content-Type': 'application/json'}
                        res = requests.post('{}/{}/_doc'.format(ELASTICSEARCH_HOST, ES_STUDY_INDEX_NAME), json=study,
                                            headers=headers)
                        print(res.json())
                        print(full_path)
                        print('==================================================================')
                except Exception as e:
                    print(e)


def add_data_objects(start_with, end_with):
    for indx in range(start_with, end_with):
        # Path to data objects folder
        directory = '/Users/iproger/sFTP/data/objects/objects{}/'.format(indx)
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                full_path = r'{}{}'.format(directory, filename)
                try:
                    with open(full_path, 'r') as opened_file:
                        json_data = json.load(opened_file)
                        data_object = data_object_converter(json_data)
                        headers = {'Content-Type': 'application/json'}
                        res = requests.post('{}/{}/_doc'.format(ELASTICSEARCH_HOST, ES_OBJECT_INDEX_NAME), json=data_object,
                                            headers=headers)
                        print(res.json())
                        print(full_path)
                        print('==================================================================')
                except Exception as e:
                    print(e)


# Start with No. of directory
# add_studies(1)
add_data_objects(10, 11)

# p = Pool(os.cpu_count())
# p.map(add_studies, range(1, 8))
# p.map(add_data_objects, range(4, 8))
