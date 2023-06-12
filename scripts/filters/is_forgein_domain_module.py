desired_domains = ['.com','.net','.org','.ca','.co.uk',
                   '.management','.biz','.us','.co','.com.au'
                   ,'edu','.nz','.pub','.uk','eu','.biz']

def is_foreign_domain(url):
    #pre-formatting url
    if str(url).endswith('/'):
        url = url[0:-2]
    for domain in desired_domains:
        if str(url).endswith(domain):
            return False
    return True

