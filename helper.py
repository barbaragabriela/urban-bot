import re
import urllib

import config


def make_pretty(text):
    try:
        terms = re.findall(r'\[(.*?)\]', text)
    except AttributeError:
        return text

    for term in terms:
        query_params = {
            'term': '{}'.format(term)
        }
        query_params = urllib.urlencode(query_params)
        query_url = config.URBAN_WEB_URL + query_params
        url = '[{}]({})'.format(term, query_url)
        text = text.replace('[{}]'.format(term), url)

    return text

