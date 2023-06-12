from google.cloud import language_v1 as lann

from .set_environment_variable import set_env_var

def get_topic_and_conf(text):
    """Classify the input text into categories."""
    set_env_var()
    language_client = lann.LanguageServiceClient()

    document = lann.Document(
        content=text, type_=lann.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document": document})
    categories = response.categories
    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence


    return result

if __name__ == '__main__':
    set_env_var()
    a = get_topic_and_conf("['', 'business how-to-stay-safe-while-gambling-in-bitcoin-casinos ', 'quotes best-anxiety-quotes ', 'marriage how-to-move-on-after-divorce-complete-guide ', 'sex-relationships how-to-make-couples-counseling-work-for-you ', 'fashion-lifestyle diy-home-improvement ', 'dating-game what-women-find-attractive-and-sexy-in-men ', 'marriage ', 'author prachi ', 'health-fitness foods-to-eat-for-better-sex-life ', 'fashion-lifestyle how-do-you-take-your-coffee ', 'quotes beyonce-quote ', 'author divya ', 'health-fitness healthy-recipes-to-try-at-home ', 'fashion-lifestyle women-invest-in-high-quality-activewear ', 'author shriya-kataria ', 'health-fitness ', 'fashion-lifestyle how-to-get-the-most-out-of-your-favorite-scents ', 'wellness benefits-of-covid-rapid-testing ', 'author angela ', 'business ways-for-businesses-to-save-money ', 'marriage la-saboteur-sabotaging-marriage ', 'sex-relationships why-men-cheat-its-more-than-sex ', 'friendship ', 'astrology ', 'shop have-clothes-but-nothing-to-wear ', 'astrology what-is-your-flower-based-on-astrological-sign ', 'family-living ', 'business ', 'rule-breakers justina-founder-of-matte-collection-a-fashion-and-swimwear-brand ', 'books 5-books-to-read-if-you-liked-the-summer-i-turned-pretty ', 'author andrew-mazur ', 'friendship when-to-call-it-quits-with-a-friend ', 'dating-game how-to-find-true-love-on-dating-apps ', 'life things-you-should-not-apologize-for ', 'author rafael ', 'author savannah-mcintosh ', 'author kate-schenk ', 'wellness allergy-symptoms-and-how-to-manage-them ', 'rule-breakers nealy-fischer-theflexiblechef ', 'astrology good-morning-and-welcome-to-december-2022 ', 'web-stories ', 'author morning ', 'entrepreneurship best-synonyms-of-entrepreneurship ', 'wellness understanding-the-practice-of-yoga-meditation-mindfulness ', 'fashion-lifestyle why-kim-kardashian-and-kanye-west-divorced ', 'life ', 'rule-breakers jalpa-pandit-jewellery ', 'wellness when-do-you-need-to-see-a-therapist ', 'wellness sleep-and-brain-supplements-boost-your-productivity ', 'quotes ', 'sex-relationships having-sex-for-the-first-time ', 'author elisabeth-goldberg ', 'author anukriti-srivastava ', 'wellness how-to-reduce-menopause-symptoms-in-the-new-year ', 'dating-game things-to-know-if-youre-tired-of-being-single ', 'parenting the-patchwork-quilt ', 'author anna-michna ', 'entrepreneurship ', 'wellness ', 'health-fitness meditation-and-hair-growth ', 'dating-game ', 'health-fitness snacks-to-tackle-mid-day-slump ', 'nft ', 'sex-relationships holiday-in-las-vegas ', 'family-living easter-celebration-tips ', 'her-journey ', 'rule-breakers preeti-luthra-pure-cimple ', 'astrology zodiac-signs-are-the-most-successful ', 'parenting ', 'health-fitness how-to-stay-healthy-this-rainy-season ', 'fashion-lifestyle difference-between-academic-writing-and-business-writing ', 'fashion-lifestyle ', 'rule-breakers parul-jain-co-founder-of-andoze ', 'author ankita ', 'author gina-handley-schmitt ', 'rule-breakers elizabeth-pearson-executive-coach ', 'our-shop ', 'sex-relationships ', 'rule-breakers ', 'about-morning-lazziness ', 'friendship what-are-the-benefits-of-having-a-guys-best-friend ', 'author abhishaik ', 'health-fitness hire-professionally-qualified-cleaners-for-schools ', 'shop ', 'author aindrila-c ', 'author mitch ', 'write-to-us ', 'books shows-to-watch-if-you-love-game-of-thrones ', 'business marketing-tips-for-bloggers-to-boost-their-blog-traffic ', 'life emotional-detachment ', 'entrepreneurship habits-to-learn-from-successful-women-leaders ', 'books books-for-better-mental-health ', 'health-fitness 7-ways-yoga-improves-posture ', 'author sayantan ', 'wellness cbd payment-methods-to-buy-delta-8-products-online ', 'parenting how-to-prepare-for-baby ', 'author sunshine2020 ', 'sex-relationships masturbation-sessions-more-enjoyable-with-cam-girls ', 'friendship how-to-move-on-from-a-broken-friendship ', 'author beth-shaw ', 'shop how-to-get-smooth-skin-with-six-daily-lazy-routines ', 'fashion-lifestyle how-to-tell-apart-high-quality-leather-jackets-from-imitation ']")
    print(a)