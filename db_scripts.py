from sqlalchemy import create_engine
from sqlalchemy.sql import text
import requests
import re
from configs import DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_PORT 
from configs import ELASTICSEARCH_HOST, ES_STUDY_INDEX_NAME, ES_OBJECT_INDEX_NAME, SCHEMA_NAME
from configs import STUDIES_JSON_TABLE_NAME, OBJECTS_JSON_TABLE_NAME, ROW_BUFFER


def db_connection():
    return create_engine('postgres://{}:{}@{}:{}/{}'.format(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))


def remove_html_tags(text):
    clean_from_tags = re.compile('<.*?>')
    text = re.sub(clean_from_tags, '', text)
    clean_from_comments = re.compile('<!--.*?-->')
    clean_text = re.sub(clean_from_comments, '', text)
    return clean_text


def name_selection(param):
    if param is not None and param['name'] is not None and param['name'] != '':
        return param['name']
    else:
        return None


def study_features_processing(study_features):
    if study_features is not None and study_features != '':
        revised_study_features = []
        for feature in study_features:
            revised_feature = {
                "id": feature['id'] if 'id' in feature else None,
                "feature_type": name_selection(feature['feature_type']) if 'feature_type' in feature else None,
                "feature_value": name_selection(feature['feature_value']) if 'feature_value' in feature else None
            }
            revised_study_features.append(revised_feature)
        return revised_study_features

    else:
        return None


def study_identifiers_processing(study_identifiers):
    revised_study_identifiers = []

    if study_identifiers is not None and study_identifiers != '':
        for ident in study_identifiers:
            identifier = {
                "id": ident['id'],
                "identifier_type": name_selection(ident['identifier_type']),
                "identifier_org": name_selection(ident['identifier_org']),
                "identifier_value": ident['identifier_value'],
                "identifier_link": ident['identifier_link'],
                "identifier_date": ident['identifier_date']
            }
            revised_study_identifiers.append(identifier)

        return revised_study_identifiers

    else:
        return None


def study_topics_processing(study_topics):
    revised_study_topics = []

    if study_topics is not None and study_topics != '':
        for topic in study_topics:
            revised_topic = {
                "id": topic['id'],
                "topic_type": name_selection(topic['topic_type']),
                "mesh_coded": topic['mesh_coded'],
                "topic_code": topic['topic_code'],
                "topic_value": topic['topic_value'],
                "topic_qualcode": topic['topic_qualcode'],
                "topic_qualvalue": topic['topic_qualvalue'],
                "original_value": topic['original_value']
            }

            revised_study_topics.append(revised_topic)

        return revised_study_topics

    else:
        return None


def study_titles_processing(study_titles):
    revised_study_titles = []

    if study_titles is not None and study_titles != '':
        for study_title in study_titles:
            revised_study_title = {
                "id": study_title['id'],
                "title_type": name_selection(study_title['title_type']),
                "title_text": study_title['title_text'],
                "lang_code": study_title['lang_code'],
                "comments": study_title['comments']
            }
            revised_study_titles.append(revised_study_title)

        return revised_study_titles
    else:
        return None


def study_relationships_processing(study_relationships):
    revised_study_relationships = []

    if study_relationships is not None and study_relationships != '':
        for relation in study_relationships:
            revised_relation = {
                "id": relation['id'],
                "relationship_type": name_selection(relation['relationship_type']),
                "target_study_id": relation['target_study_id']
            }
            revised_study_relationships.append(revised_relation)
        return revised_study_relationships
    else:
        return None


def study_converter(study):
    if study is not None:

        min_age = None
        max_age = None

        if 'min_age' in study and study['min_age'] is not None:
            min_age = {
                "value": study['min_age']['value'],
                "unit_name": study['min_age']['unit_name']
            }

        if 'max_age' in study and study['max_age'] is not None:
            max_age = {
                "value": study['max_age']['value'],
                "unit_name": study['max_age']['unit_name']
            }

        brief_description = None
        if 'brief_description' in study and study['brief_description'] is not None:
            if 'contains_html' in study['brief_description']:
                if study['brief_description']['contains_html'] is True:
                    if study['brief_description']['text'] is not None:
                        brief_description = remove_html_tags(study['brief_description']['text'])
                    else:
                        brief_description = None
                else:
                    brief_description = study['brief_description']['text']
            else:
                if 'text' in study['brief_description']:
                    brief_description = study['brief_description']['text']
                else:
                    brief_description = None

        data_sharing_statement = None
        if 'data_sharing_statement' in study and study['data_sharing_statement'] is not None:
            if 'contains_html' in study['data_sharing_statement']:
                if study['data_sharing_statement']['contains_html'] is True:
                    if study['data_sharing_statement']['text'] is not None:
                        data_sharing_statement = remove_html_tags(study['data_sharing_statement']['text'])
                    else:
                        data_sharing_statement = None
                else:
                    data_sharing_statement = study['data_sharing_statement']['text']
            else:
                if 'text' in study['data_sharing_statement']:
                    data_sharing_statement = study['data_sharing_statement']['text']
                else:
                    data_sharing_statement = None

        revised_study = {
            "id": study['id'] if 'id' in study else None,
            "display_title": study['display_title'] if 'display_title' in study else None,
            "brief_description": brief_description,
            "data_sharing_statement": data_sharing_statement,
            "study_type": name_selection(study['study_type']) if 'study_type' in study else None,
            "study_status": name_selection(study['study_status']) if 'study_status' in study else None,
            "study_gender_elig": name_selection(study['study_gender_elig']) if 'study_gender_elig' in study else None,
            "study_enrolment": study['study_enrolment'] if 'study_enrolment' in study else None,
            "min_age": min_age,
            "max_age": max_age,
            "study_identifiers": study_identifiers_processing(study['study_identifiers']) if 'study_identifiers' in study else None,
            "study_titles": study_titles_processing(study['study_titles']) if 'study_titles' in study else None,
            "study_features": study_features_processing(study['study_features']) if 'study_features' in study else None,
            "study_topics": study_topics_processing(study['study_topics']) if 'study_topics' in study else None,
            "study_relationships": study_relationships_processing(study['study_relationships']) if 'study_relationships' in study else None,
            "linked_data_objects": study['linked_data_objects'] if 'linked_data_objects' in study else None,
            "provenance_string": study['provenance_string'] if 'provenance_string' in study else None
        }
        return revised_study
    else:
        return None


def object_instances_processing(object_instances):
    if object_instances is not None:
        revised_instances = []
        for instance in object_instances:

            access_details = None
            if 'access_details' in instance and instance['access_details'] is not None:
                access_details = {
                    "direct_access": instance['access_details']['direct_access'] if 'direct_access' in instance['access_details'] else None,
                    "url": instance['access_details']['url'] if 'url' in instance['access_details'] else None,
                    "url_last_checked": instance['access_details']['url_last_checked'] if 'url_last_checked' in instance['access_details'] else None
                }

            resource_details = None
            if 'resource_details' in instance and instance['resource_details'] is not None:
                resource_details = {
                    "type_name": instance['resource_details']['type_name'] if 'type_name' in instance['resource_details'] else None,
                    "size": instance['resource_details']['size'] if 'size' in instance['resource_details'] else None,
                    "size_unit": instance['resource_details']['size_unit'] if 'size_unit' in instance['resource_details'] else None,
                    "comments": instance['resource_details']['comments'] if 'comments' in instance['resource_details'] else None
                }

            revised_instance = {
                "id": instance['id'] if 'id' in instance else None,
                "repository_org": name_selection(instance['repository_org']) if 'repository_org' in instance else None,
                "access_details": access_details,
                "resource_details": resource_details
            }

            revised_instances.append(revised_instance)

        return revised_instances

    else:
        return None


def object_url_selection(object_instances):
    object_url = None
    if object_instances is not None:
        if len(object_instances) > 0:
            if object_instances[0]['access_details']['url'] != '' and \
                    object_instances[0]['access_details']['url'] is not None:
                object_url = object_instances[0]['access_details']['url']
                return object_url
    else:
        return object_url


def object_titles_processing(object_titles):
    if object_titles is not None:
        revised_object_titles = []
        for title in object_titles:

            revised_title = {
                "id": title['id'] if 'id' in title else None,
                "title_type": name_selection(title['title_type']) if 'title_type' in title else None,
                "title_text": title['title_text'] if 'title_text' in title else None,
                "lang_code": title['lang_code'] if 'lang_code' in title else None,
                "comments": title['comments'] if 'comments' in title else None
            }
            revised_object_titles.append(revised_title)

        return revised_object_titles

    else:
        return None


def object_dates_processing(object_dates):
    if object_dates is not None:
        revised_object_dates = []
        for date in object_dates:

            start_date = None
            if 'start_date' in date and date['start_date'] is not None:
                start_date = {
                    "year": date['start_date']['start_year'] if 'start_year' in date['start_date'] else None,
                    "month": date['start_date']['start_month'] if 'start_month' in date['start_date'] else None,
                    "day": date['start_date']['start_day'] if 'start_day' in date['start_date'] else None
                }

            end_date = None
            if 'end_date' in date and date['end_date'] is not None:
                end_date = {
                    "year": date['end_date']['end_year'] if 'end_year' in date['end_date'] else None,
                    "month": date['end_date']['end_month'] if 'end_month' in date['end_date'] else None,
                    "day": date['end_date']['end_day'] if 'end_day' in date['end_date'] else None
                }

            revised_date = {
                "id": date['id'] if 'id' in date else None,
                "date_type": name_selection(date['date_type']) if 'date_type' in date else None,
                "is_date_range": date['is_date_range'] if 'is_date_range' in date else None,
                "date_as_string": date['date_as_string'] if 'date_as_string' in date else None,
                "start_date": start_date,
                "end_date": end_date,
                "comments": date['comments'] if 'comments' in date else None
            }
            revised_object_dates.append(revised_date)
        return revised_object_dates
    else:
        return None


def object_contributors_processing(object_contributors):
    if object_contributors is not None:
        revised_object_contributors = []
        for contrib in object_contributors:

            person = None
            if 'person' in contrib and contrib['person'] is not None:
                person = {
                    "family_name": contrib['person']['family_name'] if 'family_name' in contrib['person'] else None,
                    "given_name": contrib['person']['given_name'] if 'given_name' in contrib['person'] else None,
                    "full_name": contrib['person']['full_name'] if 'full_name' in contrib['person'] else None,
                    "orcid": contrib['person']['orcid'] if 'orcid' in contrib['person'] else None,
                    "affiliation": contrib['person']['affiliation'] if 'affiliation' in contrib['person'] else None
                }

            revised_contributor = {
                "id": contrib['id'] if 'id' in contrib else None,
                "contribution_type": name_selection(contrib['contribution_type']) if 'contribution_type' in contrib else None,
                "is_individual": contrib['is_individual'] if 'is_individual' in contrib else None,
                "organisation": name_selection(contrib['organisation']) if 'organisation' in contrib else None,
                "person": person
            }
            revised_object_contributors.append(revised_contributor)

        return revised_object_contributors
    else:
        return None


def object_topics_processing(object_topics):
    if object_topics is not None:
        revised_object_topics = []
        for topic in object_topics:

            revised_topic = {
                "id": topic['id'] if 'id' in topic else None,
                "topic_type": name_selection(topic['topic_type']) if 'topic_type' in topic else None,
                "mesh_coded": topic['mesh_coded'] if 'mesh_coded' in topic else None,
                "topic_code": topic['topic_code'] if 'topic_code' in topic else None,
                "topic_value": topic['topic_value'] if 'topic_value' in topic else None,
                "topic_qualcode": topic['topic_qualcode'] if 'topic_qualcode' in topic else None,
                "topic_qualvalue": topic['topic_qualvalue'] if 'topic_qualvalue' in topic else None,
                "original_value": topic['original_value'] if 'original_value' in topic else None
            }

            revised_object_topics.append(revised_topic)
        return revised_object_topics
    else:
        return None


def object_identifiers_processing(object_identifiers):
    if object_identifiers is not None:
        revised_object_identifiers = []
        for identifier in object_identifiers:

            revised_identifier = {
                "id": identifier['id'] if 'id' in identifier else None,
                "identifier_value": identifier['identifier_value'] if 'identifier_value' in identifier else None,
                "identifier_type": name_selection(identifier['identifier_type']) if 'identifier_type' in identifier else None,
                "identifier_date": identifier['identifier_date'] if 'identifier_date' in identifier else None,
                "identifier_org": name_selection(identifier['identifier_org']) if 'identifier_org' in identifier else None
            }

            revised_object_identifiers.append(revised_identifier)
        return revised_object_identifiers

    else:
        return None


def object_description_processing(object_descriptions):
    if object_descriptions is not None:
        revised_object_descriptions = []
        for description in object_descriptions:

            description_label = None
            description_text = None
            if 'contains_html' in description:
                if description['contains_html'] is True:
                    if 'description_label' in description and description['description_label'] is not None:
                        description_label = remove_html_tags(description['description_label'])
                    else:
                        description_label = None

                    if 'description_text' in description and description['description_text'] is not None:
                        description_text = remove_html_tags(description['description_text'])
                    else:
                        description_text = None
                else:
                    description_label = description['description_label'] if 'description_label' in description else None
                    description_text = description['description_text'] if 'description_text' in description else None
            else:
                description_label = description['description_label'] if 'description_label' in description else None
                description_text = description['description_text'] if 'description_text' in description else None

            revised_description = {
                "id": description['id'] if 'id' in description else None,
                "description_type": name_selection(description['description_type']) if 'description_type' in description else None,
                "description_label": description_label,
                "description_text": description_text,
                "lang_code": description['lang_code'] if 'lang_code' in description else None
            }

            revised_object_descriptions.append(revised_description)
        return revised_object_descriptions
    else:
        return None


def object_rights_processing(object_rights):
    if object_rights is not None:
        revised_object_rights = []
        for right in object_rights:

            revised_object_right = {
                "id": right['id'] if 'id' in right else None,
                "rights_name":  right['rights_name'] if 'rights_name' in right else None,
                "rights_url":  right['rights_url'] if 'rights_url' in right else None,
                "comments":  right['comments'] if 'comments' in right else None
            }
            revised_object_rights.append(revised_object_right)
        return revised_object_rights
    else:
        return None


def object_relationships_processing(object_relationships):
    if object_relationships is not None:
        revised_object_relationships = []
        for relation in object_relationships:
            revised_relation = {
                "id": relation['id'] if 'id' in relation else None,
                "relationship_type": name_selection(relation['relationship_type']) if 'relationship_type' in relation else None,
                "target_object_id": relation['target_object_id'] if 'target_object_id' in relation else None
            }
            revised_object_relationships.append(revised_relation)
        return revised_object_relationships
    else:
        return None


def data_object_converter(data_object):
    if data_object is not None:

        dataset_record_keys = None
        if 'dataset_record_keys' in data_object and data_object['dataset_record_keys'] is not None:
            dataset_record_keys = {
                "keys_type": data_object['dataset_record_keys']['keys_type'] if 'keys_type' in data_object['dataset_record_keys'] else None,
                "keys_details": data_object['dataset_record_keys']['keys_details'] if 'keys_details' in data_object['dataset_record_keys'] else None
            }

        dataset_deident_level = None
        if 'dataset_deident_level' in data_object and data_object['dataset_deident_level'] is not None:
            dataset_deident_level = {
                "deident_type": data_object['dataset_deident_level']['deident_type'] if 'deident_type' in data_object['dataset_deident_level'] else None,
                "deident_direct": data_object['dataset_deident_level']['deident_direct'] if 'deident_direct' in data_object['dataset_deident_level'] else None,
                "deident_hipaa": data_object['dataset_deident_level']['deident_hipaa'] if 'deident_hipaa' in data_object['dataset_deident_level'] else None,
                "deident_dates": data_object['dataset_deident_level']['deident_dates'] if 'deident_dates' in data_object['dataset_deident_level'] else None,
                "deident_nonarr": data_object['dataset_deident_level']['deident_nonarr'] if 'deident_nonarr' in data_object['dataset_deident_level'] else None,
                "deident_kanon": data_object['dataset_deident_level']['deident_kanon'] if 'deident_kanon' in data_object['dataset_deident_level'] else None,
                "deident_details": data_object['dataset_deident_level']['deident_details'] if 'deident_details' in data_object['dataset_deident_level'] else None
            }

        dataset_consent = None
        if 'dataset_consent' in data_object and data_object['dataset_consent'] is not None:
            dataset_consent = {
                "consent_type": data_object['dataset_consent']['consent_type'] if 'consent_type' in data_object['dataset_consent'] else None,
                "consent_noncommercial": data_object['dataset_consent']['consent_noncommercial'] if 'consent_noncommercial' in data_object['dataset_consent'] else None,
                "consent_geog_restrict": data_object['dataset_consent']['consent_geog_restrict'] if 'consent_geog_restrict' in data_object['dataset_consent'] else None,
                "consent_research_type": data_object['dataset_consent']['consent_research_type'] if 'consent_research_type' in data_object['dataset_consent'] else None,
                "consent_genetic_only": data_object['dataset_consent']['consent_genetic_only'] if 'consent_genetic_only' in data_object['dataset_consent'] else None,
                "consent_no_methods": data_object['dataset_consent']['consent_no_methods'] if 'consent_no_methods' in data_object['dataset_consent'] else None,
                "consents_details": data_object['dataset_consent']['consents_details'] if 'consents_details' in data_object['dataset_consent'] else None
            }

        revised_data_object = {
            "id": data_object['id'] if 'id' in data_object else None,
            "doi": data_object['doi'] if 'doi' in data_object else None,
            "display_title": data_object['display_title'] if 'display_title' in data_object else None,
            "version": data_object['version'] if 'version' in data_object else None,
            "object_class": name_selection(data_object['object_class']) if 'object_class' in data_object else None,
            "object_type": name_selection(data_object['object_type']) if 'object_type' in data_object else None,
            "publication_year": data_object['publication_year'] if 'publication_year' in data_object else None,
            "lang_code": data_object['lang_code'] if 'lang_code' in data_object else None,
            "managing_organisation": name_selection(data_object['managing_organisation']) if 'managing_organisation' in data_object else None,
            "access_type": name_selection(data_object['access_type']) if 'access_type' in data_object else None,
            "access_details": data_object['access_details'] if 'access_details' in data_object else None,
            "eosc_category": data_object['eosc_category'] if 'eosc_category' in data_object else None,
            "dataset_record_keys": dataset_record_keys,
            "dataset_deident_level": dataset_deident_level,
            "dataset_consent": dataset_consent,
            "object_url": object_url_selection(data_object['object_instances']) if 'object_instances' in data_object else None,
            "object_instances": object_instances_processing(data_object['object_instances']) if 'object_instances' in data_object else None,
            "object_titles": object_titles_processing(data_object['object_titles']) if 'object_titles' in data_object else None,
            "object_dates": object_dates_processing(data_object['object_dates']) if 'object_dates' in data_object else None,
            "object_contributors": object_contributors_processing(data_object['object_contributors']) if 'object_contributors' in data_object else None,
            "object_topics": object_topics_processing(data_object['object_topics']) if 'object_topics' in data_object else None,
            "object_identifiers": object_identifiers_processing(data_object['object_identifiers']) if 'object_identifiers' in data_object else None,
            "object_descriptions": object_description_processing(data_object['object_descriptions']) if 'object_descriptions' in data_object else None,
            "object_rights": object_rights_processing(data_object['object_rights']) if 'object_rights' in data_object else None,
            "object_relationships": object_relationships_processing(data_object['object_relationships']) if 'object_relationships' in data_object else None,
            "linked_studies": data_object['linked_studies'] if 'linked_studies' in data_object else None,
            "provenance_string": data_object['provenance_string'] if 'provenance_string' in data_object else None,
        }

        return revised_data_object

    else:
        return None


def studies_injection():
    engine = db_connection()
    with engine.connect() as conn:
        query = text("select * from {}.{} order by id asc".format(SCHEMA_NAME, STUDIES_JSON_TABLE_NAME))
        res = conn.execution_options(stream_results=True, max_row_buffer=ROW_BUFFER).execute(query)
        
        for partition in res:
            try:
                study = study_converter(partition[1])
                headers = {'Content-Type': 'application/json'}
                res = requests.post('{}/{}/_doc'.format(ELASTICSEARCH_HOST, ES_STUDY_INDEX_NAME), json=study,
                                    headers=headers)
                print(res.json())
                print('==================================================================')
            except Exception as e:
                print(e)


def objects_injection():
    engine = db_connection()
    with engine.connect() as conn:
        query = text("select * from {}.{} order by id asc".format(SCHEMA_NAME, OBJECTS_JSON_TABLE_NAME))
        res = conn.execution_options(stream_results=True, max_row_buffer=ROW_BUFFER).execute(query)
        
        for partition in res:
            try:
                data_object = data_object_converter(partition[1])
                headers = {'Content-Type': 'application/json'}
                res = requests.post('{}/{}/_doc'.format(ELASTICSEARCH_HOST, ES_OBJECT_INDEX_NAME), json=data_object,
                                    headers=headers)
                print(res.json())
                print('==================================================================')
            except Exception as e:
                print(e)


studies_injection()
objects_injection()
