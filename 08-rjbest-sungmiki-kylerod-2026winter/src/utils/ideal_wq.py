

def ideal_wq(df, path='data/wq.csv'):
    '''
    Feature engineer water quality columns

    input
    -----
    df: pandas dataframe
    path: str

    return
    ------
    pandas dataframe
    '''

    import pandas as pd
    import numpy as np

    # read water quality data
    df = pd.read_csv(path)
    df.describe().round().astype(int)

    # Add a column for each key value, and label it 1 if the instances value is within the ideal range, and 0 otherwise.
    df['DRP'] = [1 if _ < 100 else 0 for _ in df['dissolved reactive phosphorus']]
    df['EC'] = [1 if _ < 800 else 0 for _ in df['electrical conductance']]
    df['Alkalinity'] = [1 if _ > 20 and _ < 200 else 0 for _ in df['total alkalinity']]

    # Here are DataFrames with only ideal or undeal water quality
    ideal = df[(df['DRP']==1) & (df['EC']==1) & (df['Alkalinity']==1)]
    unideal = df[(df['DRP']==0) & (df['EC']==0) & (df['Alkalinity']==0)]

    # Add ideal/unideal columns
    df = df.assign(how_good=df['Alkalinity']+df['DRP']+df['EC'])
    df['ideal'] = np.where(df['how_good'] > 2, 1, 0)
    df['unideal'] = np.where(df['how_good'] < 1, 1, 0)

    return df