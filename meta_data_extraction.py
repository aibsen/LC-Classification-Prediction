from urllib.request import urlopen
from html.parser import HTMLParser

data_list = []
data_list_item = []

class metaDataHTMLParser(HTMLParser):

    def handle_endtag(self, tag):
        global data_list
        global data_list_item
        if tag == 'tr':
            data_list.append(data_list_item)
            data_list_item = []

    def handle_data(self, data):
        global data_list_item
        data_list_item.append(data)


html = urlopen("http://nesssi.cacr.caltech.edu/catalina/Allns.arch.html#table1")
the_page = str(html.read())


parser = meDataHTMLParser()
parser.feed(the_page)
