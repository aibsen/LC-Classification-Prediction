#This file goes to the CRTS data page and extracts all the urls of the light curves, so I can then process those.

from urllib.request import urlopen
from html.parser import HTMLParser
import csv

url_list = []

class URLHTMLParser(HTMLParser):
    #class to extract urls for lightcurves, so we can then scrap them
    global url_list
    def handle_starttag(self, tag, attrs):
        lc = "Lightcurve"
        if tag == 'a' and len(attrs) >= 1 and len(attrs[0]) >=2:
            if attrs[0][1]!= None and lc in attrs[0][1]:
                url_attr = attrs[2][1]
                #parse url
                split_attr = url_attr.split("'")
                url = split_attr[1]
                url = url[0:len(url)-1]
                url_list.append(url)

def save(url_list, file_name):
    with open(file_name, 'w') as urlFile:
        print("gonna wr this: ", url_list)
        wr = csv.writer(urlFile, lineterminator='\n')
        for url in url_list:
            wr.writerow([url])

if __name__ == "__main__":
    urls = ["http://nesssi.cacr.caltech.edu/catalina/Allns.arch.html#table1",
            "http://nesssi.cacr.caltech.edu/MLS/Allns.arch.html",
            "http://nesssi.cacr.caltech.edu/SSS/Allns.html"]
    for index, url in enumerate(urls):
        url_list = []
        html = urlopen(url)
        the_page = str(html.read())
        parser = URLHTMLParser()
        parser.feed(the_page)
        file_name = "data"+str(index)+"/lc_urls.csv"
        save(url_list, file_name)
