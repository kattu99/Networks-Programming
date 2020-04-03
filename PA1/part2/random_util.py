def parse_url(url):
    if 'http://' in url:
        url_list = url.split("/", 3)
        print(url_list)
        return url_list[2], url_list[3]
    else: 
        url_list = url.split("/", 1)
        return url_list[0], url_list[1]


print(parse_url("http://www.columbia.edu/ìge2211/4119/test3/www.engineering.columbia.edu/"))
