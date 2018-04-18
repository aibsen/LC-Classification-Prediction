from urllib.request import urlopen
from html.parser import HTMLParser
import csv

# url_list = []

# class URLHTMLParser(HTMLParser):
#     #class to extract urls for lightcurves, so we can then scrap them
#     global url_list
#     def handle_starttag(self, tag, attrs):
#         lc = "Lightcurve"
#         if tag == 'a' and len(attrs) >= 1 and len(attrs[0]) >=2:
#             if attrs[0][1]!= None and lc in attrs[0][1]:
#                 url_attr = attrs[2][1]
#                 #parse url
#                 split_attr = url_attr.split("'")
#                 url = split_attr[1]
#                 url = url[0:len(url)-1]
#                 url_list.append(url)

# def save(url_list):
#     with open("data/lc_urls.csv", 'w') as urlFile:
#         print("reached this part")
#         print("gonna wr this: ", url_list)
#         wr = csv.writer(urlFile, lineterminator='\n')
#         for url in url_list:
#             wr.writerow([url])

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

def save_lc(url,lc_point_list):
    #get name for file, which will be the id -last bit- of the url
    name = url.split("/")
    name = "data/"+name[len(name)-1].split("p")[0]
    print("Saving lc to file ", name)
    fieldnames = ["coords","date","mag","error"]
    print(name)
    with open(name, 'w') as lcFile:
        writer = csv.writer(lcFile)
        writer.writerow(fieldnames)
        writer.writerows(lc_point_list)
    
    

if __name__ == "__main__":
    with open("data/lc_urls.csv", newline='\n') as urlFile:
        reader = csv.reader(urlFile)
        for row in reader:
            url = row[0]
            print("Getting lc from ", url)
            get_page_content(url)
            save_lc(url,lc_point_list)
            lc_point_list=[]
