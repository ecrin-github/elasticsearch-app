from sqlalchemy import create_engine
from sqlalchemy.sql import text
import requests
from configs import DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_PORT
from configs import ELASTICSEARCH_HOST, ES_MDR_RECORD_INDEX_NAME, SCHEMA_NAME
from configs import STUDIES_JSON_TABLE_NAME, OBJECTS_JSON_TABLE_NAME, ROW_BUFFER


def db_connection():
    return create_engine('postgres://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))


def mdr_record_injection():
    engine = db_connection()
    with engine.connect() as conn:
        query = text("select * from {}.{} order by id asc".format(SCHEMA_NAME, STUDIES_JSON_TABLE_NAME))
        res = conn.execution_options(stream_results=True, max_row_buffer=ROW_BUFFER).execute(query)

        for partition in res:
            try:
                study = partition[1]
                if len(study['linked_data_objects']) > 0:
                    data_objects_array = []

                    obj_id_set = tuple(study['linked_data_objects'])
                    query = text("select * from {}.{} where id in :obj_id_set".format(SCHEMA_NAME, OBJECTS_JSON_TABLE_NAME))
                    res = conn.execute(query, obj_id_set=obj_id_set).fetchall()
                    if res:
                        for obj in res:
                            data_objects_array.append(obj[1])

                study['linked_data_objects'] = data_objects_array

                headers = {'Content-Type': 'application/json'}
                res = requests.post('{}/{}/_doc'.format(ELASTICSEARCH_HOST, ES_MDR_RECORD_INDEX_NAME), json=study,
                                    headers=headers)
                print(res.json())
                print('==================================================================')
            except Exception as e:
                print(e)
                break


mdr_record_injection()


def mdr_record_injection_missing():
    engine = db_connection()
    with engine.connect() as conn:
        query = text("select * from {}.{} where id=:id".format(SCHEMA_NAME, STUDIES_JSON_TABLE_NAME))
        res = conn.execution_options(stream_results=True, max_row_buffer=ROW_BUFFER).execute(query, id=3175979)

        for partition in res:
            try:
                study = partition[1]
                if len(study['linked_data_objects']) > 0:
                    data_objects_array = []

                    obj_id_set = tuple(study['linked_data_objects'])
                    query = text("select * from {}.{} where id in :obj_id_set".format(SCHEMA_NAME, OBJECTS_JSON_TABLE_NAME))
                    res = conn.execute(query, obj_id_set=obj_id_set).fetchall()
                    if res:
                        for obj in res:
                            data_objects_array.append(obj[1])

                study['linked_data_objects'] = data_objects_array

                headers = {'Content-Type': 'application/json'}
                res = requests.post('{}/{}/_doc'.format(ELASTICSEARCH_HOST, ES_MDR_RECORD_INDEX_NAME), json=study,
                                    headers=headers)
                print(res.json())
                print('==================================================================')
            except Exception as e:
                print(e)
                break


# mdr_record_injection_missing()
