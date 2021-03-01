import os
import json
import requests
import re
from multiprocessing import Pool

from elasticsearch import Elasticsearch, helpers
from configs import ELASTICSEARCH_HOST, ES_STUDY_INDEX_NAME, ES_OBJECT_INDEX_NAME


es_client = Elasticsearch([ELASTICSEARCH_HOST], verify_certs=True)


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





STUDY = {
  "file_type": "study",
  "id": 3200007,
  "display_title": "Characterizing the cerebrovAscular Physiology of Optimal Mean Arterial Pressure Targeted Resuscitation",
  "brief_description": {
    "text": "Hypoxic ischemic brain injury is a devastating illness that occurs after cardiac arrest (the heart stopping) and can yield irreversible brain damage, often leading to death. The mainstay in therapy is to optimize the delivery of oxygen to the brain to help it recover. In patients with traumatic brain injury (similar to HIBI), the investigators are able to optimize oxygen delivery to the brain with the use of wires placed into the brain that sense the pressure and oxygen in the skull to find the ideal blood pressure for each individual patient. This strategy is associated with improved outcomes. The investigators are conducting a prospective study investigating whether the perfusion within proximity to the optimal MAP is associated with improved brain oxygenation and blood flow .",
    "contains_html": None
  },
  "data_sharing_statement": None,
  "study_type": {
    "id": 11,
    "name": "Interventional"
  },
  "study_status": {
    "id": 14,
    "name": "Recruiting"
  },
  "study_enrolment": 20,
  "study_gender_elig": {
    "id": 900,
    "name": "All"
  },
  "min_age": {
    "value": 18,
    "unit_id": 17,
    "unit_name": "years"
  },
  "max_age": None,
  "provenance_string": "Data retrieved from ClinicalTrials.gov at 17:24, 01 Apr 2020",
  "study_identifiers": [
    {
      "id": 20772397,
      "identifier_value": "NCT03609333",
      "identifier_type": {
        "id": 11,
        "name": "Trial Registry ID"
      },
      "identifier_org": {
        "id": 100120,
        "name": "ClinicalTrials.gov"
      },
      "identifier_date": "2018 Jul 25",
      "identifier_link": None
    },
    {
      "id": 20772398,
      "identifier_value": "H16-00466",
      "identifier_type": {
        "id": 14,
        "name": "Sponsor ID"
      },
      "identifier_org": {
        "id": 100212,
        "name": "University of British Columbia"
      },
      "identifier_date": None,
      "identifier_link": None
    }
  ],
  "study_titles": [
    {
      "id": 20724962,
      "title_type": {
        "id": 14,
        "name": "Acronym or Abbreviation"
      },
      "title_text": "CAMPHIBIII",
      "lang_code": "en",
      "comments": None
    },
    {
      "id": 20724963,
      "title_type": {
        "id": 17,
        "name": "Protocol title"
      },
      "title_text": "Characterizing the cerebrovAscular Physiology of Optimal Mean Arterial Pressure Targeted Resuscitation in Hypoxic Ischemic Brain Injury After Cardiac Arrest",
      "lang_code": "en",
      "comments": None
    },
    {
      "id": 20724964,
      "title_type": {
        "id": 15,
        "name": "Public Title"
      },
      "title_text": "Characterizing the cerebrovAscular Physiology of Optimal Mean Arterial Pressure Targeted Resuscitation",
      "lang_code": "en",
      "comments": None
    }
  ],
  "study_topics": [
    {
      "id": 21910463,
      "topic_type": {
        "id": 13,
        "name": "condition"
      },
      "mesh_coded": True,
      "topic_code": "D006323",
      "topic_value": "Heart Arrest",
      "topic_qualcode": None,
      "topic_qualvalue": None,
      "original_value": "Heart Arrest"
    },
    {
      "id": 21910462,
      "topic_type": {
        "id": 13,
        "name": "condition"
      },
      "mesh_coded": True,
      "topic_code": "D006323",
      "topic_value": "Heart Arrest",
      "topic_qualcode": None,
      "topic_qualvalue": None,
      "original_value": "Cardiac Arrest"
    }
  ],
  "study_features": [
    {
      "id": 21403978,
      "feature_type": {
        "id": 20,
        "name": "Phase"
      },
      "feature_value": {
        "id": 100,
        "name": "Not applicable"
      }
    },
    {
      "id": 21403980,
      "feature_type": {
        "id": 21,
        "name": "Primary purpose"
      },
      "feature_value": {
        "id": 430,
        "name": "Basic Science"
      }
    },
    {
      "id": 21403977,
      "feature_type": {
        "id": 22,
        "name": "Allocation type"
      },
      "feature_value": {
        "id": 215,
        "name": "Not provided"
      }
    },
    {
      "id": 21403981,
      "feature_type": {
        "id": 23,
        "name": "Intervention model"
      },
      "feature_value": {
        "id": 300,
        "name": "Single group assignment"
      }
    },
    {
      "id": 21403979,
      "feature_type": {
        "id": 24,
        "name": "Masking"
      },
      "feature_value": {
        "id": 525,
        "name": "Not provided"
      }
    }
  ],
  "study_relationships": None,
  "linked_data_objects": [
    10340457,
    10783663,
    10843888
  ]
}


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




DATA_OBJECT = {
  "file_type": "data_object",
  "id": 10300004,
  "doi": None,
  "display_title": "Pilot Study of the Safety and Efficacy of Carvedilol in Pulmonary Arterial Hypertension :: CTG Registry entry",
  "version": None,
  "object_class": {
    "id": 23,
    "name": "Text"
  },
  "object_type": {
    "id": 13,
    "name": "Trial registry entry"
  },
  "publication_year": 2009,
  "managing_organisation": {
    "id": 100120,
    "name": "ClinicalTrials.gov"
  },
  "lang_code": "en",
  "access_type": {
    "id": 12,
    "name": "Public on-screen access"
  },
  "access_details": None,
  "eosc_category": 0,
  "provenance_string": "Data retrieved from ClinicalTrials.gov at 18:06, 01 Apr 2020",
  "dataset_record_keys": None,
  "dataset_deident_level": None,
  "dataset_consent": None,
  "object_instances": [
    {
      "id": 40331932,
      "repository_org": {
        "id": 100120,
        "name": "ClinicalTrials.gov"
      },
      "access_details": {
        "url": "https://clinicaltrials.gov/ct2/show/study/NCT00964678",
        "direct_access": True,
        "url_last_checked": None
      },
      "resource_details": {
        "type_id": 39,
        "type_name": "Web text with XML or JSON via API ",
        "size": None,
        "size_unit": None,
        "comments": None
      }
    }
  ],
  "object_titles": [
    {
      "id": 40333526,
      "title_type": {
        "id": 22,
        "name": "Study short name :: object type"
      },
      "title_text": "Pilot Study of the Safety and Efficacy of Carvedilol in Pulmonary Arterial Hypertension :: CTG Registry entry",
      "lang_code": "en",
      "comments": None
    }
  ],
  "object_contributors": [
    {
      "id": 20364881,
      "contribution_type": {
        "id": 69,
        "name": "Collaborating organisation"
      },
      "is_individual": False,
      "organisation": {
        "id": 100163,
        "name": "GlaxoSmithKline"
      },
      "person": None
    },
    {
      "id": 20316783,
      "contribution_type": {
        "id": 51,
        "name": "Study lead"
      },
      "is_individual": True,
      "organisation": None,
      "person": {
        "family_name": None,
        "given_name": None,
        "full_name": "Daniel C Grinnan",
        "orcid": None,
        "affiliation": None
      }
    },
    {
      "id": 20364882,
      "contribution_type": {
        "id": 54,
        "name": "Trial sponsor"
      },
      "is_individual": False,
      "organisation": {
        "id": 100315,
        "name": "Virginia Commonwealth University"
      },
      "person": None
    }
  ],
  "object_dates": [
    {
      "id": 40341412,
      "date_type": {
        "id": 12,
        "name": "Available"
      },
      "is_date_range": False,
      "date_as_string": "2009 Aug 25 (est.)",
      "start_date": {
        "start_year": 2009,
        "start_month": 8,
        "start_day": 25
      },
      "end_date": None,
      "comments": None
    },
    {
      "id": 40341411,
      "date_type": {
        "id": 18,
        "name": "Updated"
      },
      "is_date_range": False,
      "date_as_string": "2017 Jun 8",
      "start_date": {
        "start_year": 2017,
        "start_month": 6,
        "start_day": 8
      },
      "end_date": None,
      "comments": None
    }
  ],
  "object_topics": [
    {
      "id": 20808925,
      "topic_type": {
        "id": 12,
        "name": "Chemical / agent"
      },
      "mesh_coded": True,
      "topic_code": "D000077261",
      "topic_value": "Carvedilol",
      "topic_qualcode": None,
      "topic_qualvalue": None,
      "original_value": "Carvedilol"
    },
    {
      "id": 20808927,
      "topic_type": {
        "id": 13,
        "name": "Condition"
      },
      "mesh_coded": True,
      "topic_code": "D065627",
      "topic_value": "Familial Primary Pulmonary Hypertension",
      "topic_qualcode": None,
      "topic_qualvalue": None,
      "original_value": "Familial Primary Pulmonary Hypertension"
    },
    {
      "id": 20808926,
      "topic_type": {
        "id": 13,
        "name": "Condition"
      },
      "mesh_coded": True,
      "topic_code": "D006973",
      "topic_value": "Hypertension",
      "topic_qualcode": None,
      "topic_qualvalue": None,
      "original_value": "Hypertension"
    },
    {
      "id": 20808924,
      "topic_type": {
        "id": 13,
        "name": "Condition"
      },
      "mesh_coded": True,
      "topic_code": "D000081029",
      "topic_value": "Pulmonary Arterial Hypertension",
      "topic_qualcode": None,
      "topic_qualvalue": None,
      "original_value": "Pulmonary Arterial Hypertension"
    }
  ],
  "object_descriptions": None,
  "object_identifiers": None,
  "object_rights": None,
  "object_relationships": None,
  "linked_studies": [
    3138458
  ]
}


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


# print(json.dumps(study_converter(STUDY), indent=4))
# print(json.dumps(data_object_converter(DATA_OBJECT), indent=4))


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
