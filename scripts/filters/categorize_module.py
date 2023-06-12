import sys
sys.path.append('..')
try:
    from .detect_topic import get_topic
except:
    from detect_topic import get_topic
def categorize(url):
    categories = []
    topics = get_topic(url)
    for topic in topics:
        categories.append(topic.split('/')[1])
    return list(set(categories))
