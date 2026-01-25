import pandas as pd

def primary_dataset(landsat='landsat_features_training.csv', terraclimate='terraclimate_features_training.csv', wq='water_quality_training_dataset.csv', col='Sample Date'):
    '''
    input: 3 primary datasets (CSV files) from EY's Water Quality Prediction: Benchmark Notebook
    return: merged pandas dataframe with added bin column (monthly) joined on GPS coordinates and date
    '''
    # read CSVs
    landsat = pd.read_csv(landsat)
    terraclimate = pd.read_csv(terraclimate)
    wq = pd.read_csv(wq)

    # merge features and targets on coordinates and date; convert to datetime
    landsat_terracl = pd.merge(landsat, terraclimate)
    landsat_terracl_wq = pd.merge(landsat_terracl, wq)
    landsat_terracl_wq[col] = pd.to_datetime(landsat_terracl_wq[col], dayfirst=True, errors='coerce')

    # bin according to month
    bins = pd.date_range(start=landsat_terracl_wq[col].min(), end=landsat_terracl_wq[col].max(), freq='ME')
    landsat_terracl_wq['binned_months'] = pd.cut(landsat_terracl_wq[col], bins=len(bins), labels=bins)

    print('We will explore Water Quality over the course of',len(landsat_terracl_wq[['binned_months']].groupby('binned_months').count()),'months.')

    return landsat_terracl_wq