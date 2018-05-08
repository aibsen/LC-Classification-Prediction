import csv
import pandas as pd
import numpy as np


def load_data():
    fieldnames = ['ID', 'RA (J2000)', 'Dec (J2000)', 'UT Date', 'Mag', 'images', 'SDSS', 'Others', 'Followed', 'Last', 'LC', 'FC', 'Classification','SubClassification']
    data0 = pd.read_csv("data0/lc_metadata.csv", sep=",", names=fieldnames, skiprows=1)
    data0 = data0.drop_duplicates()
    data0["Survey"] = "CSS"
    data1 = pd.read_csv("data1/lc_metadata.csv", sep=",", names=fieldnames, skiprows=1)
    data1["Survey"] = "MLS"
    data1 = data1.drop_duplicates()
    data2 = pd.read_csv("data2/lc_metadata.csv", sep=",", names=fieldnames, skiprows=1)
    data2["Survey"] = "SSS"
    data2 = data2.drop_duplicates()
    frames = [data0, data1, data2]
    data = pd.concat(frames, ignore_index=True)
    return data

def add_tags(data):
    classes = data.groupby('Classification').count()    
    main_classes = classes[classes["ID"] > 100]
    tags = list(filter(lambda tag: not "?" in tag, list(main_classes.index)))
    data['tag'] = np.where(
        data['Classification'].isin(tags), data['Classification'], 'Other'
    )
    return data, tags

def consider_1st_class(data, tags):
    # consider all classes containing "/" as 1st class 
    data['tag'] = np.where(
        (data['Classification'].str.contains("/")) &
        (data['Classification'].str.split("/").str[0].isin(tags)), 
        data['Classification'].str.split("/").str[0], data["tag"]
    )
    return data

def ignore_question_marks(data, tags):
     # consider all classes containing "?" as if they didn't
    data['tag'] = np.where(
        (data['Classification'].str.contains('\\?',na=False)) &
        (~ data['Classification'].str.contains('/', na=False))&
        (data['Classification'].str.split("?").str[0].isin(tags)), 
        data['Classification'].str.split("?").str[0], data["tag"]
    )
    return data

def tags_to_numbers(data, tags):
    tags.append("Other")
    data['tag'] = data['tag'].map(lambda tag: tags.index(tag),
               na_action=None)
    return data, tags

if __name__ == "__main__":
    #load data
    data = load_data()
    data, tags = add_tags(data)
    data = consider_1st_class(data, tags)
    data = ignore_question_marks(data, tags) 
    data, tags = tags_to_numbers(data,tags)
    #save tagged metadata
    data.to_csv("data/tagged_meta_data.csv", sep=',')
    
