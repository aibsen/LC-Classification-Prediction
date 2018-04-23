from urllib.request import urlopen
from html.parser import HTMLParser
import csv

lc_list = []
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
    # print(url)
    # print(the_page)
    parser = LCHTMLParser()
    parser.feed(the_page)

def save_lc(url,lc_point_list, index):
    #get name for file, which will be the id -last bit- of the url
    name = url.split("/")
    name = "data"+str(index)+"/"+name[len(name)-1].split("p")[0]
    print("Saving lc to file ", name)
    fieldnames = ["coords","date","mag","error"]
    print(name)
    with open(name, 'w') as lcFile:
        writer = csv.writer(lcFile)
        writer.writerow(fieldnames)
        writer.writerows(lc_point_list)
    
    

if __name__ == "__main__":

    for index in range(3):
        with open("data"+str(index)+"/lc_urls.csv", newline='\n') as urlFile:
            reader = csv.reader(urlFile)
            for row in reader:
                url = row[0]
                print("Getting lc from ", url)
                get_page_content(url)
                save_lc(url,lc_point_list, index)
                lc_point_list=[]
