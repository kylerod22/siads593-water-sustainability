import os
import pandas as pd
import zipfile
import glob

def pop_density(path='data/Population_density'):
    
    path = 'data/Population_density'
    if not os.path.exists(path):
        dir_list = os.listdir()
        for file in dir_list:
            print(file)
            if file.endswith('.zip'):
                with zipfile.ZipFile(file) as f:
                    pd.read_csv(f)
                    

    # Get data file names
    filenames = glob.glob(path + "/*.zip") # .csv
    return filenames