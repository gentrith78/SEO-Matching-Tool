from datetime import datetime

def save_to_database_m(collection,url,categories,is_english,is_forgein_domain):
    document_model = {
        'url': url,
        'categories': categories,
        'is_english': is_english,
        'is_foreign_domain': is_forgein_domain,
        'date-time': datetime.strftime(datetime.now(), '%Y_%m_%d-%H_%M')
    }
    collection.insert_one(document_model)
    pass