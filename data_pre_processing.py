import csv
import pandas as pd
import numpy as np

if __name__ == "__main__":
    fieldnames = ['CRTS ID', 'RA (J2000)', 'Dec (J2000)', 'UT Date', 'Mag', 'CSS images', 'SDSS', 'Others', 'Followed', 'Last', 'LC', 'FC', 'Classification','SubClassification']
    data0 = pd.read_csv("data0/lc_metadata.csv", sep=",", names=fieldnames, skiprows=1)
    data1 = pd.read_csv("data1/lc_metadata.csv", sep=",", names=fieldnames, skiprows=1)
    data2 = pd.read_csv("data2/lc_metadata.csv", sep=",", names=fieldnames, skiprows=1)
    frames = [data0, data1, data2]
    data = pd.concat(frames)
    # print(data.shape)
    # get all classes
    classes = data.groupby('Classification').count()
    # get all classes with more than a hundred objects
    main_classes = classes[classes["CRTS ID"] > 100]
    # tansform that to list and remove all tags that have "?" in it
    tags = list(filter(lambda tag: not "?" in tag, list(main_classes.index)))
    print(tags)
    #add extra column to data frame with codes for tags. 
    # consider all classes containing "?" as if they didn't
    # consider all classes containing "/" as 1st class 
    # consider all other as 'Unknown'
    data['tag'] = np.where(
        # data['Classification'] in tags, tags.index(data['Classification']), None
        data['Classification'].isin(tags), data['Classification'], 'Unknown'
    )
    print(data.head)