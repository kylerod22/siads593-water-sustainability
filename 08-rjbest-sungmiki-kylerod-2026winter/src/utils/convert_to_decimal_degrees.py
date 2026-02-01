import re
import pandas as pd

# Formula: Decimal Degrees = Degrees + (Minutes ÷ 60) + (Seconds ÷ 3,600)
# For example, to convert 30° 15′ 50″: Decimal Degrees = 30 + (15 ÷ 60) + (50 ÷ 3,600) = 30.2639°.
# https://stackoverflow.com/questions/33997361/how-to-convert-degree-minute-second-to-degree-decimal

def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(3600)
    if direction == 'W' or direction == 'S': # West and south are negative
        dd *= -1
    return dd

# def dd2dms(deg):
#     d = int(deg)
#     md = abs(deg - d) * 60
#     m = int(md)
#     sd = (md - m) * 60
#     return [d, m, sd]

def parse_dms(dms):
    parts = re.split('[^\d\w]+', dms) # split on ° ' "

    try:
        lat = dms2dd(parts[0], parts[1], parts[2], parts[3])
    except:
        lat = dms
    return (lat)


def convert_to_decimal_degrees(series: pd.Series) -> pd.DataFrame:
    '''
    Docstring for convert_to_decimal_degrees
    returns: TRY pandas datafram with two columns of floats (EXCEPT some may not be floats)
    '''

    df = series.str.split(' / ', n=1, expand=True)
    df = df[0].str.split(' ', n=1, expand=True)
    df.columns = ['latitude', 'longitude']

    df['latitude'] = df['latitude'].apply(lambda x: parse_dms(x))
    df['longitude'] = df['longitude'].apply(lambda x: parse_dms(x))

    return df