# Function for cleaning the 2 files of data (csv downloaded from 2017 to 2021)
# https://www.ree.es/en/datos/generation/generation-structure

import pandas as pd
def cleaning(csvname):

    # Read the csv file
    df = pd.read_csv("data/"+ csvname,encoding="latin-1")

    # Fit/Rename the columns
    new_header = ['Type', '2017', '2018', '2019', '2020', '2021']
    df.columns = new_header

    # Removing rows with "NaN"/row with no valid values/ set colum "Type" as index
    df = df.dropna(how='any',axis=0)
    df = df.drop([8], axis=0)
    df = df.drop([3], axis=0)
    df.set_index("Type")

    # Transform the object to float
    df[['2017', '2018', '2019', '2020', '2021']] = df[['2017', '2018', '2019', '2020', '2021']].applymap(lambda x: float(x.replace(",", ".")))
    df[['2017', '2018', '2019', '2020', '2021']] = df[['2017', '2018', '2019', '2020', '2021']].applymap(lambda x: round(x,2))

    return df
