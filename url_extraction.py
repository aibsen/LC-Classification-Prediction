from urllib.request import urlopen
from html.parser import HTMLParser

html = urlopen("http://nesssi.cacr.caltech.edu/catalina/Allns.arch.html#table1")
the_page = str(html.read())
url_list = []

class URLHTMLParser(HTMLParser):
    #class to extract urls for lightcurves, so we can then scrap them
    def handle_starttag(self, tag, attrs):
        lc = "Lightcurve"
        if tag == 'a' and len(attrs) >= 1 and len(attrs[0]) >=2:
            if attrs[0][1]!= None and lc in attrs[0][1]:
                url_attr = attrs[2][1]
                #parse url
                split_attr = url_attr.split("'")
                url = split_attr[1]
                url = url[0:len(url)-1]
                print(url)

parser = URLHTMLParser()
parser.feed(the_page)
