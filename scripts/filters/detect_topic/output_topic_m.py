from .get_input_data_p import get_subcategories, get_MainPage_text
from .get_topic_and_confidence_p import get_topic_and_conf
"""
This package will be responsible to get the raw text data for api
This package can return subcategories and first page text
It takes an url_in and mode as input
"mode" is an integer that tells this package what data to return.
mode 1: Returns subcategories
mode 2: Returns first page text
"""

"""
TOPIC VERIFYING ALGORITHM
if the confidence from the categorization is lower than .7 and higher than .5 initiate the first page text search but add the topic outputted from categorization algorithms
so whenever there is a confidence beetwen .5 and .7 it should be added as a topic, but proceed to other method, when is higher, it should add the topic but do not proceed  with other method
"""

MINIMAL_THRESHHOLD = 0.5
STANDARD_THRESHHOLD = 0.7




def get_topic(url):
    topics = []
    should_i_try_other_input = False
    # get subcategories text
    subcategories_text_preProcessed = get_subcategories(url)
    # Call Api
    try:
        subcategories_text_apiCall = dict(get_topic_and_conf(subcategories_text_preProcessed))
        if len(subcategories_text_apiCall) == 0:
            should_i_try_other_input = True
        for topic in subcategories_text_apiCall:
            if float(subcategories_text_apiCall[topic]) >= MINIMAL_THRESHHOLD:
                if float(subcategories_text_apiCall[topic]) < STANDARD_THRESHHOLD:
                    should_i_try_other_input = True
                topics.append(topic)
    except Exception as e:
        should_i_try_other_input = True
    # checking if going with main page text as input is necessary
    if should_i_try_other_input:
        try:
            mainPage_text_preProcessed = get_MainPage_text(url)
            mainPage_text_apiCall = dict(get_topic_and_conf(mainPage_text_preProcessed))
            for topic in mainPage_text_apiCall:
                if float(mainPage_text_apiCall[topic])> MINIMAL_THRESHHOLD:
                    topics.append(topic)
        except Exception as e:
            pass
    return list(set(topics))
