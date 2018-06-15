from urllib.request import urlopen
from html.parser import HTMLParser
import csv

lc_point_list=[]

class LCHTMLParser(HTMLParser):
    #class to parse the actual lightcurves
    global lc_point_list
    def handle_starttag(self, tag, attrs):
        if tag == 'area':
            #get coordinates
            coords = attrs[1][1] 
            #get date, mag, error
            point = attrs[2][1] 
            xye = point.split(";")
            clean_point=[]
            for i in xye:
                separate = i.split("'")
                if len(separate) > 1:
                    item = separate[1] 
                    l = len(item)
                    clean_item = item[0:l-1]
                    clean_point.append(clean_item)
            date = clean_point[0]
            mag = clean_point[1]
            error = clean_point[2]
            lc_point_list.append([coords, date, mag, error])


def get_page_content(url): 
    html = urlopen(url)
    the_page = str(html.read())
    parser = LCHTMLParser()
    parser.feed(the_page)

def save_lc(url,lc_point_list):
    #get name for file, which will be the id -last bit- of the url
    name = url.split("/")
    name = "data/transients/"+name[len(name)-1].split("p")[0]+".csv"
    print("Saving lc to file ", name)
    fieldnames = ["coords","date","mag","error"]
    with open(name, 'w') as lcFile:
        writer = csv.writer(lcFile)
        writer.writerow(fieldnames)
        writer.writerows(lc_point_list)

def transient_lc_extraction(fin):
    global lc_point_list
    reader = csv.reader(fin)
    name = ""
    for url in fin:
        print("getting LC from ", url)
        get_page_content(url)
        save_lc(url, lc_point_list)
        lc_point_list=[]