from urllib.request import urlopen
from html.parser import HTMLParser
import csv
from pipeline_utils import crts_url_list

data_list = []
data_list_item = []
meta_data_list = []

class metaDataHTMLParser(HTMLParser):

    def handle_endtag(self, tag):
        global data_list
        global data_list_item
        if tag == 'tr':
            data_list.append(data_list_item)
            print(data_list_item)
            data_list_item = []

    def handle_data(self, data):
        global data_list_item
        # print(str(data))
        data_list_item.append(str(data))

def transient_metadata_extraction():
    global data_list
    urls = crts_url_list
    for index, url in enumerate(urls):
        html = urlopen(url)
        the_page = str(html.read())
        parser = metaDataHTMLParser()
        parser.feed(the_page)
        data_list = data_list[1:]
        #remove junk
        for item in data_list:
            item.pop(0)
            id = item.pop(0)
            id = id[:len(id)-2]
            item.insert(0,id)
            item.pop(12)
        # # #write to file11
        # # save_meta_data(data_list, index)
        meta_data_list.append(data_list)
        data_list = []
    flat_list = [item for sublist in meta_data_list for item in sublist]
    return flat_list