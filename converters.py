from studies import *
from data_objects import *


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

        revised_study = {
            "id": study['id'] if 'id' in study else None,
            "display_title": study['display_title'] if 'display_title' in study else None,
            "brief_description": study['brief_description'] if 'brief_description' in study else None,
            "data_sharing_statement": study['data_sharing_statement'] if 'data_sharing_statement' in study else None,
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
