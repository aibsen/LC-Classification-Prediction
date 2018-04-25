import csv
import pandas as pd
import numpy as np

if __name__ == "__main__":
    #load data
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
    #concat data
    data = pd.concat(frames, ignore_index=True)
    #check for duplicated objects
    # duplicated = data.duplicated(subset="ID")
    # isDuplicated = duplicated[duplicated == True]
    # duplicated_rows = data.loc[isDuplicated.keys()]["ID"]

    # get all classes
    classes = data.groupby('Classification').count()    
    # get all classes with more than a hundred objects
    main_classes = classes[classes["ID"] > 100]
    # tansform that to list and remove all tags that have "?" in it
    tags = list(filter(lambda tag: not "?" in tag, list(main_classes.index)))
    #add extra column to data frame with codes for tags. 
    # consider all other as 'Unknown'
    data['tag'] = np.where(
        data['Classification'].isin(tags), data['Classification'], 'Other'
    )
    # consider all classes containing "/" as 1st class 
    data['tag'] = np.where(
        (data['Classification'].str.contains("/")) &
        (data['Classification'].str.split("/").str[0].isin(tags)), 
        data['Classification'].str.split("/").str[0], data["tag"]
    )
    # consider all classes containing "?" as if they didn't
    data['tag'] = np.where(
        (data['Classification'].str.contains('\\?',na=False)) &
        (~ data['Classification'].str.contains('/', na=False))&
        (data['Classification'].str.split("?").str[0].isin(tags)), 
        data['Classification'].str.split("?").str[0], data["tag"]
    )
    # convert tags to numbers
    tags.append("Other")
    data['tag'] = data['tag'].map(lambda tag: tags.index(tag),
               na_action=None)

    #save tagged metadata
    data.to_csv("tagged_meta_data.csv", sep=',')
    
