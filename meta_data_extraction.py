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



if __name__ == "__main__":
    html = urlopen("http://nesssi.cacr.caltech.edu/catalina/Allns.arch.html#table1")
    the_page = str(html.read())
    parser = meDataHTMLParser()
    parser.feed(the_page)

    # def get_lc(url):
    #     html = urlopen(url)
    #     lc_page = str(html.read())


    metaDataFileName = "data/lc_metadata.csv"
    with open("data/lc_urls.csv", 'wb') as urlFile:
        wr = csv.writer(metaDataFileName)
        wr.writerows(data_list)
 