from common_functions import name_selection


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
