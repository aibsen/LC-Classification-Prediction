import csv
import pandas as pd
import numpy as np
import sys
from pipeline_utils import transient_fieldnames, variables_fieldnames
import pickle as pkl


def tag_merge_metadata(output):
    variables = pd.read_csv("data/metadata/variables_lc_metadata.dat", sep=" ", skiprows=3)
    variables = variables.iloc[:,0:]
    variables = process_variables(variables)

    transients = pd.read_csv("data/metadata/transient_lc_metadata.csv", sep=",", names=transient_fieldnames, skiprows=1)
    transients = process_transients(transients)

    frames = [variables, transients]
    data = pd.concat(frames, ignore_index=True)
    print(data)
    data.to_pickle(output)

def process_transients(data):
    data = data[["CSS images", "RA", "Dec", "Classification"]]
    data.columns = ["ID","RA","Dec","SubType"]
    data = data.assign(Type =1)
    data, tags = fewer_tags(data)
    data = tags_to_numbers(data, tags)
    return data

def process_variables(data):
    #add the first line that was mistakenly loaded as header
    first_row = list(data.columns)
    data.loc[len(data)] = first_row
    #drop unnecessary columns
    data = data.iloc[:,:8]
    data.columns = variables_fieldnames
    data = data[["ID", "RA", "Dec", "SubType"]]
    data = data.assign(Type = 0)
    return data

def fewer_tags(data):
    # classes = data.groupby('SubType').count()    
    # main_classes = classes[classes["ID"] > 100]
    # tags = list(filter(lambda tag: not "?" in tag, list(main_classes.index)))
    #consider only the following classes 
    tags = ["AGN","Blazar","CV","Flare","SN"]
    data['SubType'] = np.where(
        data['SubType'].isin(tags), data['SubType'], 'Unknown/Other'
    )
    return data, tags

def tags_to_numbers(data, tags):
    tags.append('Unknown/Other')
    data['SubType'] = data['SubType'].map(lambda tag: tags.index(tag),
               na_action=None)
    return data

# def consider_1st_class(data, tags):
#     # consider all classes containing "/" as 1st class 
#     data['SubType'] = np.where(
#         (data['SubType'].str.contains("/")) &
#         (data['SubType'].str.split("/").str[0].isin(tags)), 
#         data['SubType'].str.split("/").str[0], data["SubType"]
#     )
#     return data

# def ignore_question_marks(data, tags):
#     # consider all classes containing "?" as if they didn't
#     data['SubType'] = np.where(
#         (data['SubType'].str.contains('\\?',na=False)) &
#         (~ data['SubType'].str.contains('/', na=False))&
#         (data['SubType'].str.split("?").str[0].isin(tags)), 
#         data['SubType'].str.split("?").str[0], data["SubType"]
#     )
#     return data




