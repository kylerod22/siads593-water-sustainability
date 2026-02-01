import pandas as pd

landsat_path = 'data/ey_ai_datasets/landsat_features.csv'
terraclimate_path = 'data/ey_ai_datasets/terraclimate_features.csv'
wq_path = 'data/ey_ai_datasets/water_quality_dataset.csv'

def primary_dataset(landsat=landsat_path, terraclimate=terraclimate_path, wq=wq_path, col='Sample Date'):
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
    landsat_terracl_wq['month'] = pd.cut(landsat_terracl_wq[col], bins=len(bins), labels=bins)

    # Handling Missing Values
    wq_data = landsat_terracl_wq.fillna(landsat_terracl_wq.median(numeric_only=True))
    wq_data.isna().sum()
    wq_data.columns = wq_data.columns.str.strip().str.lower()

    print('We will explore Water Quality over the course of',len(wq_data[['month']].groupby('month', observed=True).count()),'months.')

    return wq_data