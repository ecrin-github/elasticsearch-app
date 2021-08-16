import re


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
