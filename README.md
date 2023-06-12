# SEO Filter Tool: 
This app is a series of python scripts working with each other to present a UI to the user so the user can select the filters that need to be processed for a specific list of websites.
Basically user inputs a worksheet URL and enables 'Anyone with the link' permission, then user lists the targeted websites URL in the first column and applies the rules in the app. The app will create new columns to show the categories of each website accordingly and will map if it is a match or not.

There are 3 filters that have been implemented:
 - First filter is the category of website (news, sport, tv ...etc). The app will get the html source from a 
    target website, will analyze text content, will use some NLP processes like:**Lemmatiztion process**, **Stop word removal**,**Removing unnecessary words (privacy&policy, contact-us...***
Then it will send this text to google api which will return the text category/website category
- Second filter is to check the language of the website, again i use same text that i send to google but instead of google NLP I use 'langdetect' library to get the language of the text.
- Third filter is the to check if the website has a foreign domain.

## Quickstart

- Use Python 3.1 or newer
- Open your terminal and go to this directory
- Install PIP requirements
- Launch UI

```console
python3 -m pip install -r requirements.txt
python3 ocr_launcher.py
```

### Dependencies
- **Mongodb:** Fill credentials in *scripts/settings.py*
- **Web Scraping API** Enter Api token in *scripts/settings.py*
- **NLP Service** Place credentials json file in *scripts\filters\detect_topic\get_topic_and_confidence_p\service_account_credentials* 
- **Google Sheets API** Place credentials json file in *scripts\google_sheet_service\service_account_creds* 

### Technologies Implemented:
- **Database**: Mongodb
- **Web Scraping API Service**: Scrape do
- **NLP Service:** Google Nlp Api
- **Google Sheets API** 


### Cautions
- In the input google spreadsheet make sure that enable anyone with link and the permission is changed to Editor
- In the input google spreadsheet make sure that the sheet you want to process is lined up first among other sheets

