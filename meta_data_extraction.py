from urllib.request import urlopen
from html.parser import HTMLParser
import csv

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

def save_meta_data(data_list):
    with open("data/lc_metadata.csv", 'w') as metaDataFile:
        wr = csv.writer(metaDataFile)
        fieldnames = ['CRTS ID', 'RA (J2000)', 'Dec (J2000)', 'UT Date', 'Mag', 'CSS images', 'SDSS', 'Others', 'Followed', 'Last', 'LC', 'FC', 'Classification']
        wr.writerow(fieldnames)
        wr.writerows(data_list)
   

if __name__ == "__main__":
    html = urlopen("http://nesssi.cacr.caltech.edu/catalina/Allns.arch.html#table1")
    the_page = str(html.read())
    parser = metaDataHTMLParser()
    parser.feed(the_page)
    data_list = data_list[1:]
    for item in data_list:
    # remove unnecessary line jumps
        item.pop(0)
        id = item.pop(0)
        id = id[:len(id)-2]
        item.insert(0,id)
    #write to file
    save_meta_data(data_list)