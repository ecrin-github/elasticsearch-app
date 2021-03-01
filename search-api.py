from elasticsearch import Elasticsearch


def es_connection():
    elasticsearch_host = 'http://localhost:9200/'
    return Elasticsearch([elasticsearch_host], verify_certs=True)


def specific_study_search(identifier_type, identifier_value):

    es_client = es_connection()

    query_body = {
        "query": {
            "nested": {
                "path": "study_identifiers",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    'study_identifiers.identifier_type.id': identifier_type,
                                },
                            },
                            {
                                "term": {
                                    'study_identifiers.identifier_value': identifier_value
                                }
                            }
                        ],
                    },
                }
            }
        }
    }

    result = es_client.search(index="study", body=query_body)

    objects = []

    for obj in result['hits']['hits']:
        objects.append(obj['_source'])

    print(objects)

    return objects


specific_study_search(11, "NCT00070486")


def study_characteristics(title_contains, operator, topics_include):

    es_client = es_connection()

    query_condition = "must"

    if operator == "and":
        query_condition = "must"
    else:
        query_condition = "should"

    query_body = {
        "query": {
            "bool": {
                "should": [{
                    "simple_query_string": {
                        "query": title_contains,
                        "fields": ["display_title.title_text"],
                        "default_operator": "and",
                    },
                }, {
                    "nested": {
                        "path": "study_titles",
                        "query": {
                            "simple_query_string": {
                                "query": title_contains,
                                "fields": ["study_titles.title_text"],
                                "default_operator": "and",
                            },
                        },
                    },
                }],
                query_condition: {
                    "nested": {
                        "path": 'study_topics',
                        "query": {
                            "simple_query_string": {
                                "query": topics_include,
                                "fields": ['study_topics.topic_value'],
                                "default_operator": "and",
                            },
                        },
                    },
                },
            },
        }
    }

    result = es_client.search(index='study', body=query_body)

    objects = []

    for obj in result['hits']['hits']:
        objects.append(obj['_source'])

    print(objects)

    return objects


# study_characteristics("COVID", "and", "HEART")


def via_published_paper(search_type, value):
    es_client = es_connection()

    query_body = {}

    if search_type == "doi":
        query_body = {
            "query": {
                "bool": {
                    "must": {
                        "term": {
                            "doi": value
                        }
                    }
                }
            }
        }

    elif search_type == "title":
        query_body = {
            "query": {
                "bool": {
                    "must": [{
                        "bool": {
                            "filter": [{
                                "term": {
                                    #Journal article
                                    "object_type.id": 12,
                                },
                            }],
                            "should": [{
                                "simple_query_string": {
                                    "query": value,
                                    "fields": ["display_title"],
                                    "default_operator": "and",
                                },
                            }, {
                                "nested": {
                                    "path": "object_titles",
                                    "query": {
                                        "simple_query_string": {
                                            "query": value,
                                            "fields": ["object_titles.title_text"],
                                            "default_operator": "and",
                                        },
                                    },
                                },
                            }],
                            "minimum_should_match": 1,
                        },
                    }]
                }
            }
        }

    result = es_client.search(index='data-object', body=query_body)

    objects = []

    for obj in result['hits']['hits']:
        objects.append(obj['_source'])

    print(objects)

    return objects


# via_published_paper("doi", "10.1136/bjsports-2015-094603")


def get_fetched_study(study_id):
    es_client = es_connection()

    query_body = {
        "query": {
            "match": {
                "id": study_id
            }
        }
    }

    result = es_client.search(index='study', body=query_body)

    print(result['hits']['hits'][0]['_source'])

    # return result['hits']['hits'][0]['_source']


# get_fetched_study(3010003)
