from sqlalchemy import create_engine
from sqlalchemy.sql import text
import requests
from configs import DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_PORT
from configs import ELASTICSEARCH_HOST, ES_STUDY_INDEX_NAME, ES_OBJECT_INDEX_NAME, SCHEMA_NAME
from configs import STUDIES_JSON_TABLE_NAME, OBJECTS_JSON_TABLE_NAME, ROW_BUFFER


def db_connection():
    return create_engine('postgres://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))


def studies_injection():
    has_error = False
    engine = db_connection()
    with engine.connect() as conn:
        query = text("select * from {}.{} order by id asc".format(SCHEMA_NAME, STUDIES_JSON_TABLE_NAME))
        res = conn.execution_options(stream_results=True, max_row_buffer=ROW_BUFFER).execute(query)
        
        for partition in res:
            try:
                headers = {'Content-Type': 'application/json'}
                res = requests.post('{}/{}/_doc'.format(ELASTICSEARCH_HOST, ES_STUDY_INDEX_NAME), json=partition[1],
                                    headers=headers)
                print(res.json())
                has_error = False
                print('==================================================================')
            except Exception as e:
                has_error = True
                print(e)
                break

            if has_error:
                break


def objects_injection():
    has_error = False
    engine = db_connection()
    with engine.connect() as conn:
        query = text("select * from {}.{} order by id asc".format(SCHEMA_NAME, OBJECTS_JSON_TABLE_NAME))
        res = conn.execution_options(stream_results=True, max_row_buffer=ROW_BUFFER).execute(query)
        
        for partition in res:
            try:
                headers = {'Content-Type': 'application/json'}
                res = requests.post('{}/{}/_doc'.format(ELASTICSEARCH_HOST, ES_OBJECT_INDEX_NAME), json=partition[1],
                                    headers=headers)
                has_error = False
                print(res.json())
                print('==================================================================')
            except Exception as e:
                has_error = True
                print(e)
                break

            if has_error:
                break


studies_injection()
objects_injection()
