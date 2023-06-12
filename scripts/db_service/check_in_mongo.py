def check_database_m(collection,url):
    match = (collection.find_one({'url':url}))
    if match != None:
        data_of_url = {
            'categories': match['categories'],
            'is_english': match['is_english'],
            'is_foreign_domain': match['is_foreign_domain']
        }
        return data_of_url
    return None