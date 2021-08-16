from common_functions import name_selection


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
