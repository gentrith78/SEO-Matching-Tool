import spacy


"""
This function willl be responsible to pre-process the text for google nlp api so it will input only neccesary elemtns/words.
Processes:
    lemmatiztion process
    stop word removal
    removing unnecesary words (privacy&policy, contact-us...)
    
This function accepts only list as an input
"""

def pre_process_TEXT(text:list):
    lemmatized = []
    nlp = spacy.load("en_core_web_sm")
    stop_words_ = nlp.Defaults.stop_words
    for el in text:
        if el == '' or str(el).isspace() or str(el).isdigit():
            continue
        this_lemma = []
        doc = nlp(str(el).replace('-',' '))
        for token in doc:
            if token.text.lower() not in stop_words_:
                this_lemma.append(token.lemma_)
            # this_lemma.append(token.lemma_)
        lemmatized.append(' '.join(this_lemma).rstrip().lstrip())
    return str(lemmatized)
    pass


if __name__ == '__main__':
    a= ['', 'Contact us', 'Communicative', 'Our results are presented in dollars and cents. We don’t try to justify our work with clicks, referrals, engagement, or rankings no one cares about.', '535 5TH AVE', 'NEW YORK, NY, 10017', '291%MORE CALLS', 'Learn how SearchTides increased SEO traffic and helped this hotel chain compete with some of the largest competitors in the world.', ' 9 moPERIOD', '161 BOOKINGS', '“I wish I knew what was actually happening during my SEO campaign. I just sit and hope that my rankings go up.”', 'BLOG', 'Learn how healthcare giant Medtronic used SearchTides after an acquisition with Covidien to retain rankings, create new ones, and drive a 45% increase in traffic.', ' $71,885/mo REVENUE', 'Our core principles', 'Ready for the SEO you deserve?', ' 9 month PERIOD', 'APPLY', '45%TRAFFIC GROWTH', '“I want to feel like a valued client – I need an agency who will be proactive and in touch with us at regular intervals.”', 'SearchTides was able to nearly quadruple the SEO phone calls for a client in an industry riddled with black hat SEO tactics. SEO revenue increased nearly $15,000 a month.', 'ROI Driven', 'Process', 'ROI', 'SEARCHTIDES', '“I wish the value driven from our SEO could be tracked in dollars and cents.”', '4TH FLOOR', 'SearchTides is not the right partner for every company, but we are the perfect partner for some. Find out if a budding relationship is meant to be.', 'You’re in the hands of professionals. A seamless onboarding process, detailed status reports, and regular checks in will keep you constantly updated.', 'Comms', 'Case studiesENTERPRISEMIDSIZELOCAL', 'Dedicated to SEO', '252% GROWTH', '300NEW KEYWORDS', 'Copyright © 2023 SearchTides', '(855) SRCH-TDS', 'MIDSIZE', '4 monthPERIOD', '$19,805/moSEO REVENUE', 'LOCAL', 'ENTERPRISE', '42% LiftNON SEO REV', '90,428/moNEW VISITORS', 'Instead of claiming expertise in everything, SearchTides focuses exclusively on Search Engine Optimization. This focus led to our fully transparent process.']
    print(a)
    print(len(str(a)))
    lematized = pre_process_TEXT(a)
    print(len(lematized))
    print(lematized)